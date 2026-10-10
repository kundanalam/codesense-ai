from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.problems import PROBLEMS
from backend.detect.analyze import analyze
from backend.teach.hints import get_hint
from backend.teach.leakage import check_hint

app = FastAPI(title="CodeSense AI")

# Lets the frontend (running on another address) call this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    problem_id: str
    code: str


class HintRequest(BaseModel):
    problem_id: str
    code: str
    level: int = 1


@app.get("/problems")
def list_problems():
    return [
        {
            "problem_id": pid,
            "title": p["title"],
            "description": p["description"],
            "starter_code": p["starter_code"],
        }
        for pid, p in PROBLEMS.items()
    ]


@app.post("/analyze")
def analyze_code(req: AnalyzeRequest):
    if req.problem_id not in PROBLEMS:
        return {"error": "Unknown problem_id"}
    return analyze(req.code, req.problem_id)


@app.post("/hint")
def hint(req: HintRequest):
    if req.problem_id not in PROBLEMS:
        return {"error": "Unknown problem_id"}

    diagnosis = analyze(req.code, req.problem_id)
    level = max(1, min(4, req.level))

    if diagnosis["status"] == "correct":
        return {
            "hint_level": level,
            "hint": "Your code passed all tests. Nice work!",
            "leakage_blocked": False,
            "max_level": 4,
            "status": "correct",
        }

    if diagnosis["status"] in ("syntax_error", "timeout"):
        text = diagnosis["explanation"]
    else:
        text = get_hint(diagnosis, level)

    reference = PROBLEMS[req.problem_id]["reference"]
    text, blocked = check_hint(text, reference)

    return {
        "hint_level": level,
        "hint": text,
        "leakage_blocked": blocked,
        "max_level": 4,
        "status": diagnosis["status"],
        "error_type": diagnosis["error_type"],
    }
from typing import List, Optional
from backend.detect.analyze_free import analyze_free


class Example(BaseModel):
    input: str
    expected: str


class FreeRequest(BaseModel):
    code: str
    func: Optional[str] = None
    examples: Optional[List[Example]] = None


@app.post("/analyze_free")
def analyze_any_code(req: FreeRequest):
    examples = [e.dict() for e in req.examples] if req.examples else None
    return analyze_free(req.code, req.func, examples)