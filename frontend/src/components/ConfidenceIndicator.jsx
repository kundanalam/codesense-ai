const TIERS = [
  { min: 0.8, label: 'High confidence', cls: 'conf--high' },
  { min: 0.5, label: 'Medium confidence', cls: 'conf--mid' },
  { min: 0, label: 'Low confidence', cls: 'conf--low' },
];

export default function ConfidenceIndicator({ value }) {
  const valid = typeof value === 'number' && Number.isFinite(value) && value >= 0 && value <= 1;

  if (!valid) {
    return (
      <div className="conf">
        <div className="conf__row">
          <span className="field-label">Confidence</span>
          <span className="muted">Not available</span>
        </div>
      </div>
    );
  }

  const pct = Math.round(value * 100);
  const tier = TIERS.find((t) => value >= t.min);

  return (
    <div className={`conf ${tier.cls}`}>
      <div className="conf__row">
        <span className="field-label">Confidence</span>
        <span className="conf__value">{pct}%</span>
      </div>
      <div
        className="conf__track"
        role="progressbar"
        aria-label="Diagnosis confidence"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={pct}
      >
        <div className="conf__fill" style={{ width: `${pct}%` }} />
      </div>
      <p className="conf__caption">{tier.label}</p>
    </div>
  );
}
