# CodeSense AI: Python Programming Tutor

A tutor for beginners that finds the misconception behind buggy Python code and gives progressive hints without revealing the answer.

## What it does
- Runs the student's code safely in a sandbox with a timeout
- Finds the smallest failing input (fuzzing and shrinking)
- Detects 8 common misconceptions using AST rules
- Gives 4 levels of hints, checked by a leakage detector
- Works on 8 built-in problems (full diagnosis) and on any pasted code (free mode)

## Setup
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```
Open http://127.0.0.1:8000/docs to try the API.

## Endpoints
- GET /problems
- POST /analyze
- POST /hint
- POST /analyze_free

## Reproduce the results
```
python -m backend.eval.run_eval          # template bugs
python -m backend.eval.run_human_eval    # hand-written bugs
python -m backend.eval.run_leakage       # leakage rate
python test_problems.py                  # reference solutions pass
```

## Results
| Test | Result | Note |
|---|---|---|
| 32 template bugs | 32/32 | Pipeline check only (circular) |
| 16 hand-written bugs, before fixes | 12/16 (75%) | Honest first result |
| 16 hand-written bugs, after fixes | 16/16 | Rules were tuned on these |
| Leakage rate (256 hints) | 0% | Hints contain no code |
| Leakage checker on full solutions | 5/8 first, 8/8 after fix | |

## Limitations
- Full diagnosis works only for the 8 built-in problems; free mode cannot judge correctness without an example.
- Rules are heuristics: unusual coding styles may get generic hints.
- The hand-written test set is small (16 bugs) and the rules were tuned on it.
- Free-mode hints are not passed through the leakage checker.

## Datasets and tools
No external datasets. Python standard library, FastAPI, Uvicorn.

| 12 held-out bugs (not used for tuning) | 7/12 (58%) | Headline number; 5 misses analysed above |