# CodeMentor

A programming tutor that explains **why** your code fails (misconception detection) and guides you with a **progressive hint ladder** instead of handing you the fixed code.

Built with React + Vite (JavaScript), plain CSS and Lucide icons.

## Quick start (Windows, VS Code, PowerShell)

1. Install Node.js LTS from https://nodejs.org (check with `node -v`).
2. Open the `codementor` folder in VS Code, then open a terminal (**Terminal > New Terminal**).
3. PowerShell may block `npm.ps1`, so use `npm.cmd`:

```powershell
npm.cmd install
Copy-Item .env.example .env
npm.cmd run dev
```

The app opens at http://localhost:5173.

If PowerShell complains about scripts, you can also run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Demo mode vs. live backend

| Setting | Where | Effect |
| --- | --- | --- |
| `VITE_DEMO_MODE=true` | `.env` | App starts in Demo Mode (built-in **DEMO DATA**, no backend needed) |
| `VITE_DEMO_MODE=false` | `.env` | App starts in Live Mode (calls the real backend) |
| Header toggle | UI | Flip between demo and live at any time |
| `VITE_API_BASE_URL` | `.env` | Backend base URL, e.g. `http://localhost:8000` |

Restart `npm.cmd run dev` after editing `.env`.

Demo results are labeled **DEMO DATA** in the diagnosis panel. In Live Mode, failures are shown as errors; they are never replaced with fake results.

## Backend contract

`POST ${VITE_API_BASE_URL}/analyze`

Request:

```json
{ "language": "python", "code": "numbers = [1, 2, 3, 4, 5]\nprint(numbers[5])" }
```

Response (all nine fields):

```json
{
  "status": "error",
  "error_type": "Index Out of Range",
  "line": 2,
  "explanation": "Beginner-friendly explanation",
  "minimal_failing_input": "Minimal failing program or input",
  "expected_output": "Expected behavior",
  "actual_output": "Observed behavior or error",
  "confidence": 0.96,
  "hints": ["Hint one", "Hint two", "Hint three"]
}
```

Notes for the backend teammate:

- Enable CORS for `http://localhost:5173`.
- `status` is `success`, `error` or `warning`. `line` is a 1-based integer (or `null`). `confidence` is 0 to 1.
- Missing or invalid fields are tolerated and shown as "Not available".
- Hints containing code fences (```) are dropped by the frontend, so never put full solutions in hints.

## Project structure

```
src/
  components/
    Header.jsx               brand + demo/live switch
    CodeEditor.jsx           editor with line numbers, highlighting, error-line band
    DiagnosisPanel.jsx       status, error type, line, explanation, failing input
    OutputComparison.jsx     expected vs actual output
    ConfidenceIndicator.jsx  validated confidence bar
    HintLadder.jsx           reveal-one-at-a-time hints
  services/analysisApi.js    the only file that talks to the backend; validates responses
  data/demoDiagnosis.js      DEMO DATA
  App.jsx, App.css, main.jsx, index.css
```

## Testing checklist

1. Start in demo mode and press **Analyze Code**. You should see a loading state, then the **DEMO DATA** diagnosis.
2. Confirm all nine fields: status badge, error type title, line (and highlighted line 2 in the editor), explanation, failing input, expected vs actual output, confidence bar, hints.
3. Press **Reveal Next Hint** three times. Only one hint appears per click; the button disables after the third. **Reset Hints** locks them again.
4. Press **Reset**, then **Analyze Code** with an empty editor to see the validation message.
5. Turn demo mode off with no backend running to see the network error state.

## Safety

Student code is never executed in the browser; it is only sent to the backend.
