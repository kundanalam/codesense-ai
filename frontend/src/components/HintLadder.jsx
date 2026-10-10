import { useState } from 'react';
import { Lightbulb, Lock, RotateCcw, Eye } from 'lucide-react';

const LEVELS = [
  { title: 'Gentle Nudge', note: 'Reconsider the concept' },
  { title: 'Directional Hint', note: 'Where to look' },
  { title: 'Strong Hint', note: 'The rule behind the bug' },
];

function levelInfo(index) {
  return LEVELS[index] || { title: 'Extra Hint', note: 'Additional clue' };
}

/**
 * Hints stay hidden until revealed. Only the revealed slice is ever rendered,
 * so later hints never appear in the visible DOM early.
 * The parent should give this component a `key` so it resets on each new analysis.
 */
export default function HintLadder({ hints }) {
  const [revealed, setRevealed] = useState(0);
  const total = hints.length;
  const allRevealed = revealed >= total;

  return (
    <section className="card" aria-labelledby="hints-title">
      <div className="card__head">
        <h2 id="hints-title" className="card__title">Hint ladder</h2>
        <span className="hint-count" aria-live="polite">
          {revealed} of {total} revealed
        </span>
      </div>

      {total === 0 ? (
        <p className="muted">Not available. No hints were provided for this diagnosis.</p>
      ) : (
        <>
          <div
            className="hint-progress"
            role="progressbar"
            aria-label="Hints revealed"
            aria-valuemin={0}
            aria-valuemax={total}
            aria-valuenow={revealed}
          >
            {hints.map((_, i) => (
              <span key={i} className={i < revealed ? 'is-on' : ''} />
            ))}
          </div>

          <ol className="hints">
            {hints.map((hint, i) => {
              const info = levelInfo(i);
              const open = i < revealed;
              return (
                <li key={i} className={`hint ${open ? 'hint--open' : 'hint--locked'}`}>
                  <span className="hint__icon" aria-hidden="true">
                    {open ? <Lightbulb size={16} /> : <Lock size={16} />}
                  </span>
                  <div className="hint__body">
                    <div className="hint__title">
                      Hint {i + 1} <span className="hint__level">· {info.title}</span>
                    </div>
                    {open ? (
                      <p className="hint__text">{hint}</p>
                    ) : (
                      <p className="hint__locked">Locked. {info.note}.</p>
                    )}
                  </div>
                </li>
              );
            })}
          </ol>

          <div className="hint-actions">
            <button
              type="button"
              className="btn btn--primary"
              onClick={() => setRevealed((n) => Math.min(n + 1, total))}
              disabled={allRevealed}
            >
              <Eye size={16} aria-hidden="true" />
              {allRevealed ? 'All hints revealed' : 'Reveal Next Hint'}
            </button>
            <button
              type="button"
              className="btn btn--ghost"
              onClick={() => setRevealed(0)}
              disabled={revealed === 0}
            >
              <RotateCcw size={16} aria-hidden="true" />
              Reset Hints
            </button>
          </div>
        </>
      )}
    </section>
  );
}
