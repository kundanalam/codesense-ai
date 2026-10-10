import { useRef, useState } from 'react';
import { AlertTriangle, FileCode2, Loader2, Play, RotateCcw, Sparkles, Terminal } from 'lucide-react';
import Header from './components/Header.jsx';
import CodeEditor from './components/CodeEditor.jsx';
import DiagnosisPanel from './components/DiagnosisPanel.jsx';
import HintLadder from './components/HintLadder.jsx';
import { analyzeCode, DEFAULT_DEMO_MODE } from './services/analysisApi.js';
import { DEMO_CODE } from './data/demoDiagnosis.js';

const LANGUAGES = [
  { value: 'python', label: 'Python', supported: true },
  { value: 'javascript', label: 'JavaScript (coming soon)', supported: false },
  { value: 'java', label: 'Java (coming soon)', supported: false },
  { value: 'cpp', label: 'C++ (coming soon)', supported: false },
];

function EmptyState() {
  return (
    <section className="card state state--empty">
      <span className="state__icon"><Terminal size={26} aria-hidden="true" /></span>
      <h2 className="state__title">Your diagnosis will appear here</h2>
      <p className="muted">
        Paste some buggy code, then press <strong>Analyze Code</strong>. You'll get an explanation of the
        misconception plus hints you can reveal one at a time.
      </p>
    </section>
  );
}

function LoadingState() {
  return (
    <section className="card" aria-busy="true" aria-live="polite">
      <div className="state__loading">
        <Loader2 size={18} className="spin" aria-hidden="true" />
        <span>Analyzing your code…</span>
      </div>
      <div className="skeleton skeleton--title" />
      <div className="skeleton" />
      <div className="skeleton skeleton--short" />
      <div className="skeleton skeleton--block" />
    </section>
  );
}

function ErrorState({ error, onRetry }) {
  return (
    <section className="card state state--error" role="alert">
      <span className="state__icon state__icon--error"><AlertTriangle size={26} aria-hidden="true" /></span>
      <h2 className="state__title">Analysis failed</h2>
      <p className="field__text">{error.message}</p>
      <button type="button" className="btn btn--primary" onClick={onRetry}>
        <Play size={16} aria-hidden="true" />
        Try again
      </button>
    </section>
  );
}

export default function App() {
  const [code, setCode] = useState(DEMO_CODE);
  const [language, setLanguage] = useState('python');
  const [demoMode, setDemoMode] = useState(DEFAULT_DEMO_MODE);
  const [phase, setPhase] = useState('idle'); // idle | loading | success | error
  const [result, setResult] = useState(null); // { diagnosis, source, code, id }
  const [error, setError] = useState(null);
  const [validation, setValidation] = useState('');

  const requestId = useRef(0);
  const editorRef = useRef(null);

  const lineCount = code.split('\n').length;
  // Only highlight while the editor still matches the code that was analyzed.
  const highlightLine =
    phase === 'success' && result && result.code === code ? result.diagnosis.line : null;
  const codeChanged = phase === 'success' && result && result.code !== code;

  async function handleAnalyze() {
    if (!code.trim()) {
      setValidation('Please paste or type some code before analyzing.');
      editorRef.current?.focus();
      return;
    }
    setValidation('');
    setError(null);
    setPhase('loading');
    const id = ++requestId.current;

    try {
      const { diagnosis, source } = await analyzeCode({ language, code, demoMode });
      if (id !== requestId.current) return; // a newer request or reset happened
      setResult({ diagnosis, source, code, id });
      setPhase('success');
    } catch (err) {
      if (id !== requestId.current) return;
      setError({ message: err.message || 'Something went wrong.', kind: err.kind || 'unknown' });
      setPhase('error');
    }
  }

  function handleReset() {
    requestId.current += 1; // ignore any in-flight request
    setCode('');
    setResult(null);
    setError(null);
    setValidation('');
    setPhase('idle');
    editorRef.current?.focus();
  }

  function handleCodeChange(next) {
    setCode(next);
    if (validation) setValidation('');
  }

  const loading = phase === 'loading';

  return (
    <div className="app">
      <Header demoMode={demoMode} onToggleDemo={() => setDemoMode((v) => !v)} />

      <main className="container">
        <section className="hero">
          <p className="hero__eyebrow"><Sparkles size={14} aria-hidden="true" /> Programming tutor</p>
          <h1 className="hero__title">Understand your bugs. Improve your logic.</h1>
          <p className="hero__text">
            CodeMentor doesn't hand you the fixed code. It explains the misconception behind your bug,
            shows the smallest input that breaks it, and gives you hints one step at a time so you learn
            to fix it yourself.
          </p>
        </section>

        <div className="layout">
          <div className="layout__col">
            <section className="card" aria-labelledby="editor-title">
              <div className="card__head">
                <h2 id="editor-title" className="card__title">Your code</h2>
                <div className="lang">
                  <label htmlFor="language" className="sr-only">Programming language</label>
                  <select
                    id="language"
                    className="select"
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    disabled={loading}
                  >
                    {LANGUAGES.map((l) => (
                      <option key={l.value} value={l.value} disabled={!l.supported}>{l.label}</option>
                    ))}
                  </select>
                </div>
              </div>

              <CodeEditor
                ref={editorRef}
                value={code}
                onChange={handleCodeChange}
                highlightLine={highlightLine}
                disabled={loading}
                language={language}
              />

              {validation && (
                <p className="validation" role="alert">
                  <AlertTriangle size={16} aria-hidden="true" />
                  {validation}
                </p>
              )}
              {codeChanged && (
                <p className="note">You edited the code since the last analysis. Analyze again for an updated diagnosis.</p>
              )}

              <div className="actions">
                <button type="button" className="btn btn--primary btn--lg" onClick={handleAnalyze} disabled={loading}>
                  {loading ? (
                    <><Loader2 size={18} className="spin" aria-hidden="true" /> Analyzing…</>
                  ) : (
                    <><Play size={18} aria-hidden="true" /> Analyze Code</>
                  )}
                </button>
                <button type="button" className="btn btn--ghost" onClick={handleReset} disabled={loading}>
                  <RotateCcw size={16} aria-hidden="true" /> Reset
                </button>
                <button
                  type="button"
                  className="btn btn--ghost"
                  onClick={() => handleCodeChange(DEMO_CODE)}
                  disabled={loading}
                >
                  <FileCode2 size={16} aria-hidden="true" /> Load example
                </button>
              </div>
              <p className="safety">Your code is sent for analysis only. It is never run in your browser.</p>
            </section>
          </div>

          <div className="layout__col">
            {phase === 'idle' && <EmptyState />}
            {phase === 'loading' && <LoadingState />}
            {phase === 'error' && error && <ErrorState error={error} onRetry={handleAnalyze} />}
            {phase === 'success' && result && (
              <>
                <DiagnosisPanel diagnosis={result.diagnosis} source={result.source} lineCount={lineCount} />
                <HintLadder key={result.id} hints={result.diagnosis.hints} />
              </>
            )}
          </div>
        </div>
      </main>

      <footer className="footer">CodeMentor · built for learning, not for copying answers.</footer>
    </div>
  );
}
