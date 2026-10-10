import { forwardRef, useRef } from 'react';

const LINE_HEIGHT = 22;
const PAD_TOP = 12;

const KEYWORDS = new Set([
  'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class',
  'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global',
  'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise',
  'return', 'try', 'while', 'with', 'yield',
]);

const BUILTINS = new Set([
  'print', 'len', 'range', 'int', 'str', 'float', 'list', 'dict', 'set', 'tuple', 'bool',
  'input', 'sum', 'min', 'max', 'abs', 'sorted', 'enumerate', 'zip', 'map', 'filter',
  'open', 'type', 'isinstance', 'append',
]);

const TOKEN_RE =
  /(#[^\n]*)|("""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)/g;

/** Tiny Python highlighter: returns React nodes. Never executes the code. */
function highlightPython(text) {
  const out = [];
  let last = 0;
  let prev = null;
  let key = 0;

  for (const m of text.matchAll(TOKEN_RE)) {
    if (m.index > last) out.push(text.slice(last, m.index));
    const [tok, com, str, num, ident] = m;
    let cls = null;

    if (com) cls = 'tok-com';
    else if (str) cls = 'tok-str';
    else if (num) cls = 'tok-num';
    else if (ident) {
      if (KEYWORDS.has(ident)) cls = 'tok-kw';
      else if (prev === 'def' || prev === 'class') cls = 'tok-def';
      else if (BUILTINS.has(ident)) cls = 'tok-bi';
    }

    prev = ident === 'def' || ident === 'class' ? ident : null;
    out.push(cls ? <span key={key++} className={cls}>{tok}</span> : tok);
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(text.slice(last));
  out.push('\n'); // keeps the last (possibly empty) line visible
  return out;
}

const CodeEditor = forwardRef(function CodeEditor(
  { value, onChange, highlightLine, disabled = false, language = 'python' },
  ref
) {
  const tabEnabled = useRef(true);
  const lines = value.split('\n');
  const lineCount = lines.length;
  const showBand = highlightLine && highlightLine <= lineCount;

  function handleKeyDown(e) {
    if (e.key === 'Escape') {
      // Lets keyboard users leave the editor with Tab afterwards.
      tabEnabled.current = false;
      return;
    }
    if (e.key === 'Tab' && !e.shiftKey && tabEnabled.current) {
      e.preventDefault();
      const ta = e.target;
      const start = ta.selectionStart;
      const end = ta.selectionEnd;
      onChange(value.slice(0, start) + '    ' + value.slice(end));
      requestAnimationFrame(() => {
        ta.selectionStart = ta.selectionEnd = start + 4;
      });
    }
  }

  return (
    <div className="editor">
      <div className="editor__bar">
        <span className="editor__dots" aria-hidden="true">
          <i /><i /><i />
        </span>
        <span className="editor__file">main.{language === 'python' ? 'py' : 'txt'}</span>
        <span className="editor__meta">{lineCount} {lineCount === 1 ? 'line' : 'lines'}</span>
      </div>

      <div className="editor__scroll">
        <div className="editor__gutter" aria-hidden="true">
          {lines.map((_, i) => (
            <div key={i} className={highlightLine === i + 1 ? 'is-hit' : ''}>{i + 1}</div>
          ))}
        </div>

        <div className="editor__code">
          {showBand && (
            <div
              className="editor__band"
              style={{ top: PAD_TOP + (highlightLine - 1) * LINE_HEIGHT }}
              aria-hidden="true"
            />
          )}
          <pre className="editor__pre" aria-hidden="true">{highlightPython(value)}</pre>
          <textarea
            ref={ref}
            className="editor__textarea"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            onBlur={() => { tabEnabled.current = true; }}
            disabled={disabled}
            spellCheck={false}
            autoCapitalize="off"
            autoCorrect="off"
            wrap="off"
            aria-label="Code editor"
            aria-describedby="editor-help"
            placeholder="# Paste or type your Python code here"
          />
        </div>
      </div>
      <p id="editor-help" className="editor__help">
        Tab inserts spaces. Press Esc, then Tab, to move focus out of the editor.
      </p>
    </div>
  );
});

export default CodeEditor;
