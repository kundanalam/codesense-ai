import { CheckCircle2, XCircle } from 'lucide-react';

function Side({ variant, icon, title, text }) {
  return (
    <div className={`compare__side compare__side--${variant}`}>
      <div className="compare__head">
        {icon}
        <span>{title}</span>
      </div>
      {text ? (
        <pre className="codeblock codeblock--plain">{text}</pre>
      ) : (
        <p className="muted">Not available</p>
      )}
    </div>
  );
}

export default function OutputComparison({ expected, actual }) {
  return (
    <div className="compare">
      <Side
        variant="expected"
        icon={<CheckCircle2 size={16} aria-hidden="true" />}
        title="Expected output"
        text={expected}
      />
      <Side
        variant="actual"
        icon={<XCircle size={16} aria-hidden="true" />}
        title="Actual output"
        text={actual}
      />
    </div>
  );
}
