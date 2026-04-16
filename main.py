# -*- coding: utf-8 -*-
"""Vrutha Sahayi web — FastAPI wrapper around the ported 0.1 engine."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from vruthasahayi import data, interface
from vruthasahayi.matra import getMatraArray
from vruthasahayi.nearest_vrutham import nearest_catalog_matches

app = FastAPI(title="Vrutha Sahayi Web", version="1.0.0")


def _line_gl_patterns_for_find(gl_array):
    """Same segmentation as findvrutham.findVrutham: non-empty pieces between |."""
    gl_string = "".join(gl_array) + "|"
    gl_lines = gl_string.split("|")
    gl_lines = gl_lines[: len(gl_lines) - 1]
    return [i for i in gl_lines if i != ""]

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
if STATIC.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")


class AnalyzeBody(BaseModel):
    text: str = Field(..., description="Malayalam poem in Unicode; use newlines between lines, blank line between ślokas.")
    mode: str = Field("find", description="'find' or 'check'")
    vrutham: str = Field("", description="Meter name as shown in the list, e.g. നമ്പൂരി[13], required for check mode.")


def _format_find(rows, line_patterns):
    out = []
    for idx, row in enumerate(rows):
        sloka, line, line_vid, sloka_vid, y_ok = row
        name = ""
        if line_vid >= 0 and line_vid < len(data.vruthamTable):
            name = data.vruthamTable[line_vid][1]
        pat = ""
        if idx < len(line_patterns):
            pat = line_patterns[idx]
        nearest = []
        if line_vid < 0 and pat:
            nearest = nearest_catalog_matches(pat, top_k=5)
        item = {
            "sloka": sloka,
            "line": line,
            "lineVruthamId": line_vid,
            "lineVruthamNameMl": name,
            "slokaVruthamId": sloka_vid,
            "yathiOk": y_ok,
            "glPattern": pat,
            "nearestMatches": nearest,
        }
        out.append(item)
    return out


def _format_check(err_locs, mod_array, text):
    """Map error markers to rough character spans (best-effort)."""
    issues = []
    for i, ch in enumerate(err_locs):
        if ch == "|":
            continue
        if i < len(mod_array):
            span, status = mod_array[i]
            if span == (-1, -1):
                continue
            a, b = span
            snippet = text[a : b + 1] if a >= 0 and b >= 0 else ""
            issues.append(
                {
                    "index": i,
                    "marker": ch,
                    "status": status,
                    "start": a,
                    "end": b,
                    "snippet": snippet,
                }
            )
    return issues


@app.get("/")
def index():
    index_path = STATIC / "index.html"
    if index_path.is_file():
        return FileResponse(index_path)
    return {"message": "Place static/index.html or open /docs"}


@app.get("/api/vruthams")
def list_vruthams():
    return {"names": data.vruthamNameList()}


@app.post("/api/analyze")
def analyze(body: AnalyzeBody):
    text = body.text
    if body.mode == "check":
        if not body.vrutham.strip():
            return {"error": "Select a vrutham (meter) for check mode."}
        err, mod = interface.getVrutham(text, body.vrutham)
        if isinstance(err, str):
            return {"error": err, "mode": "check"}
        return {
            "mode": "check",
            "rawErrors": err,
            "issues": _format_check(err, mod, text),
        }

    gl_array, _ = getMatraArray(text)
    line_patterns = _line_gl_patterns_for_find(gl_array)
    rows, mod = interface.getVrutham(text, "")
    if isinstance(rows, str):
        return {"error": rows, "mode": "find"}
    return {
        "mode": "find",
        "lines": _format_find(rows, line_patterns),
        "modHints": len(mod),
    }
