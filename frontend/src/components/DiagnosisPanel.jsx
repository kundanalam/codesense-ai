import { AlertTriangle, CheckCircle2, HelpCircle, MapPin, XCircle, FlaskConical } from 'lucide-react';
import ConfidenceIndicator from './ConfidenceIndicator.jsx';
import OutputComparison from './OutputComparison.jsx';

const STATUS = {
  success: { label: 'Success', cls: 'badge--success', Icon: CheckCircle2 },
  error: { label: 'Error', cls: 'badge--error', Icon: XCircle },
  warning: { label: 'Warning', cls: 'badge--warning', Icon: AlertTriangle },
  unknown: { label: 'Unknown status', cls: 'badge--unknown', Icon: HelpCircle },
};

export default function DiagnosisPanel({ diagnosis, source, lineCount }) {
  const d = diagnosis;
  const status = STATUS[d.status] || STATUS.unknown;
  const StatusIcon = status.Icon;

  const title = d.error_type || (d.status === 'success' ? 'No issue detected' : 'Not available');
  const lineOutside = d.line !== null && d.line > lineCount;

  return (
    <section className="card" aria-labelledby="diagnosis-title">
      {source === 'demo' && (
        <div className="demo-banner" role="note">
          <FlaskConical size={16} aria-hidden="true" />
          <span>
            <strong>DEMO DATA</strong>: this diagnosis is built into the app and was not produced by a
            real analysis.
          </span>
        </div>
      )}

      <div className="card__head">
        <h2 className="card__title">Diagnosis</h2>
        <span className={`badge ${status.cls}`}>
          <StatusIcon size={14} aria-hidden="true" />
          {status.label}
        </span>
      </div>

      <h3 id="diagnosis-title" className="diagnosis__title">{title}</h3>

      <div className="diagnosis__line">
        <MapPin size={15} aria-hidden="true" />
        {d.line === null ? (
          <span className="muted">Line: Not available</span>
        ) : (
          <span>
            Likely problem on <strong>line {d.line}</strong>
            {lineOutside && <span className="muted"> (outside your current code)</span>}
          </span>
        )}
      </div>

      <div className="field">
        <span className="field-label">What went wrong</span>
        {d.explanation ? <p className="field__text">{d.explanation}</p> : <p className="muted">Not available</p>}
      </div>

      <div className="field">
        <span className="field-label">Smallest input that shows the problem</span>
        {d.minimal_failing_input ? (
          <pre className="codeblock">{d.minimal_failing_input}</pre>
        ) : (
          <p className="muted">Not available</p>
        )}
      </div>

      <OutputComparison expected={d.expected_output} actual={d.actual_output} />

      <ConfidenceIndicator value={d.confidence} />
    </section>
  );
}
