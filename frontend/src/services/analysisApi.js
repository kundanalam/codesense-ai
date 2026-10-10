import { demoDiagnosis } from '../data/demoDiagnosis.js';

// ---------------------------------------------------------------------------
// Configuration (all backend settings live here, nowhere else in the app)
// ---------------------------------------------------------------------------
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '');
const ANALYZE_PATH = '/analyze_free';
const REQUEST_TIMEOUT_MS = 30000;

/** Initial demo-mode value, from VITE_DEMO_MODE (defaults to true). */
export const DEFAULT_DEMO_MODE =
  String(import.meta.env.VITE_DEMO_MODE ?? 'true').toLowerCase() !== 'false';

export const API_URL_DISPLAY = API_BASE_URL ? `${API_BASE_URL}${ANALYZE_PATH}` : null;

// ---------------------------------------------------------------------------
// Errors
// ---------------------------------------------------------------------------
export class AnalysisError extends Error {
  /** kind: 'config' | 'network' | 'timeout' | 'http' | 'malformed' */
  constructor(message, kind = 'unknown') {
    super(message);
    this.name = 'AnalysisError';
    this.kind = kind;
  }
}

// ---------------------------------------------------------------------------
// Validation / normalization
// ---------------------------------------------------------------------------
const VALID_STATUSES = ['success', 'error', 'warning'];
const STATUS_MAP = {
  correct: 'success',
  no_error_found: 'success',
  syntax_error: 'error',
  runtime_error: 'error',
  timeout: 'error',
  logic_error: 'warning',
  bad_example: 'warning',
};

function asText(value) {
  if (value === null || value === undefined) return null;
    if (Array.isArray(value)) {
    return JSON.stringify(value.length === 1 && Array.isArray(value[0]) ? value[0] : value);
  }
  if (typeof value === 'string') return value.trim() === '' ? null : value;
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  return null;
}

function asLine(value) {
  const n = typeof value === 'string' ? Number(value) : value;
  return Number.isInteger(n) && n >= 1 ? n : null;
}

function asConfidence(value) {
  const n = typeof value === 'string' && value.trim() !== '' ? Number(value) : value;
  if (typeof n !== 'number' || !Number.isFinite(n) || n < 0) return null;
  if (n <= 1) return n;
  if (n <= 100) return n / 100; // backend sent a percentage
  return null; // out of range: better to show nothing than something misleading
}

function asHints(value) {
  if (!Array.isArray(value)) return [];
  return value
    .map((h) => (typeof h === 'string' ? h.trim() : ''))
    .filter((h) => h.length > 0)
    // Safety net: a hint must never carry a full code solution.
    .filter((h) => !h.includes('```'));
}

/**
 * Turns whatever the backend returned into the exact nine fields the UI expects.
 * Missing/invalid values become null (or [] for hints) so the UI can show fallbacks.
 */
export function normalizeDiagnosis(raw) {
  if (raw === null || typeof raw !== 'object' || Array.isArray(raw)) {
    throw new AnalysisError('The server returned an unexpected response format.', 'malformed');
  }
   let status = STATUS_MAP[String(raw.status).toLowerCase()] || 'unknown';
  if (raw.status === 'no_error_found' && raw.error_type) status = 'warning';
  return {
    status,
    error_type: asText(raw.error_type),
    line: asLine(raw.line),
    explanation: asText(raw.explanation),
    minimal_failing_input: asText(raw.minimal_failing_input),
    expected_output: asText(raw.expected_output),
    actual_output: asText(raw.actual_output),
    confidence: asConfidence(raw.confidence),
    hints: asHints(raw.hints),
  };
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Analyze student code.
 * Returns { diagnosis, source } where source is 'demo' or 'api'.
 * Throws AnalysisError on any failure (never returns fake data in live mode).
 */
export async function analyzeCode({ language, code, demoMode }) {
  if (demoMode) {
    await sleep(900); // simulate latency so loading states can be tested
    return { diagnosis: normalizeDiagnosis(structuredClone(demoDiagnosis)), source: 'demo' };
  }

  if (!API_BASE_URL) {
    throw new AnalysisError(
      'No backend URL configured. Set VITE_API_BASE_URL in your .env file and restart the dev server, or switch on Demo Mode.',
      'config'
    );
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${ANALYZE_PATH}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ language, code }),
      signal: controller.signal,
    });
  } catch (err) {
    if (err?.name === 'AbortError') {
      throw new AnalysisError('The analysis took too long and was cancelled. Please try again.', 'timeout');
    }
    throw new AnalysisError(
      `Could not reach the backend at ${API_BASE_URL}. Check that it is running and that CORS is enabled.`,
      'network'
    );
  } finally {
    clearTimeout(timer);
  }

  if (!response.ok) {
    let detail = '';
    try {
      const body = await response.json();
      detail = typeof body?.detail === 'string' ? body.detail : typeof body?.message === 'string' ? body.message : '';
    } catch {
      /* body was not JSON; ignore */
    }
    throw new AnalysisError(
      `The server responded with HTTP ${response.status}${response.statusText ? ` ${response.statusText}` : ''}.${detail ? ` ${detail}` : ''}`,
      'http'
    );
  }

  let data;
  try {
    data = await response.json();
  } catch {
    throw new AnalysisError('The server response was not valid JSON.', 'malformed');
  }

  return { diagnosis: normalizeDiagnosis(data), source: 'api' };
}
