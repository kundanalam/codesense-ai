// DEMO DATA ONLY.
// This object is NOT produced by a real backend analysis. It exists so the UI can be
// developed and tested before the backend is ready. It is only used when Demo Mode is ON.

export const DEMO_CODE = 'numbers = [1, 2, 3, 4, 5]\nprint(numbers[5])';

export const demoDiagnosis = {
  status: 'error',
  error_type: 'Index Out of Range',
  line: 2,
  explanation:
    'Python list indexing starts at 0. A list containing five elements has valid indexes from 0 to 4, so attempting to access index 5 causes an error.',
  minimal_failing_input: 'numbers = [1, 2, 3, 4, 5]\nprint(numbers[5])',
  expected_output:
    'The intended output depends on which list element the student wants to access.',
  actual_output: 'IndexError: list index out of range',
  confidence: 0.96,
  hints: [
    'Think about how Python numbers the positions in a list.',
    'Remember that the first element has index 0.',
    'Count the valid indexes in a list containing five elements.',
  ],
};
