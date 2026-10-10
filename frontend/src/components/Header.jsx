import { Bug } from 'lucide-react';
import { API_URL_DISPLAY } from '../services/analysisApi.js';

export default function Header({ demoMode, onToggleDemo }) {
  return (
    <header className="header">
      <div className="header__inner">
        <div className="brand">
          <span className="brand__logo" aria-hidden="true">
            <Bug size={20} />
          </span>
          <span className="brand__name">CodeMentor</span>
        </div>

        <div className="mode">
          <span className={`mode__badge ${demoMode ? 'mode__badge--demo' : 'mode__badge--live'}`}>
            {demoMode ? 'DEMO MODE' : 'LIVE API'}
          </span>
          <button
            type="button"
            role="switch"
            aria-checked={demoMode}
            aria-label="Demo mode"
            className={`switch ${demoMode ? 'switch--on' : ''}`}
            onClick={onToggleDemo}
            title={
              demoMode
                ? 'Using built-in demo data. Click to use the real backend.'
                : `Calling ${API_URL_DISPLAY || 'no backend configured'}. Click to use demo data.`
            }
          >
            <span className="switch__thumb" />
          </button>
          <span className="mode__label">Demo mode</span>
        </div>
      </div>
    </header>
  );
}
