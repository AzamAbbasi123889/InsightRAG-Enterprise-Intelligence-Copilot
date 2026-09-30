import { useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [question, setQuestion] = useState('Why did Europe revenue decline in Q3, and which products contributed most?')
  const [result, setResult] = useState(null)
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetch(`${API}/api/metrics`).then(r => r.json()).then(setMetrics).catch(() => {})
  }, [])

  async function ask() {
    setLoading(true)
    try {
      const r = await fetch(`${API}/api/query`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({question, top_k:5})})
      setResult(await r.json())
    } catch (e) {
      setResult({answer:'Backend is not running. Start FastAPI on port 8000.', sources:[]})
    } finally { setLoading(false) }
  }

  return <div className="page">
    <header className="hero">
      <div>
        <div className="eyebrow">ENTERPRISE AI / RAG</div>
        <h1>InsightRAG</h1>
        <p>Enterprise knowledge + structured data intelligence in one analyst copilot.</p>
      </div>
      <div className="badge">FastAPI · React · SQL · GraphRAG</div>
    </header>

    <section className="query-card">
      <label>Ask an enterprise question</label>
      <textarea value={question} onChange={e=>setQuestion(e.target.value)} rows="4"/>
      <div className="actions"><button onClick={ask} disabled={loading}>{loading ? 'Analyzing…' : 'Run analysis'}</button><span>Router selects document, SQL, or hybrid retrieval.</span></div>
    </section>

    {result && <section className="grid">
      <div className="panel answer"><div className="panel-head"><h2>Answer</h2><span className="pill">{result.intent || 'query'}</span></div><pre>{result.answer}</pre></div>
      <div className="panel"><h2>Evidence</h2>{result.sources?.map(s=><div className="source" key={s.id}><div className="source-top"><b>{s.title}</b><span>{s.source_type} · {Number(s.score).toFixed(2)}</span></div><p>{s.snippet}</p><code>{s.id}</code></div>)}</div>
    </section>}

    <section className="metrics">
      <h2>RAG Quality Dashboard</h2>
      <div className="metric-grid">
        {metrics && Object.entries(metrics).filter(([k])=>k.includes('estimate') || k.includes('latency')).map(([k,v])=><div className="metric" key={k}><div>{k.replaceAll('_',' ')}</div><strong>{typeof v==='number' && v<1 ? `${(v*100).toFixed(0)}%` : typeof v==='number' ? `${v} ms` : v}</strong></div>)}
      </div>
    </section>
  </div>
}

export default App
