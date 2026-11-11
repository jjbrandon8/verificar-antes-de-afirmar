"""Automatic working log for the verum plugin (verificar antes de afirmar).

Claude Code calls this script after every batch of tool calls (PostToolBatch)
and after every failed tool call (PostToolUseFailure). It appends one line per
tool call to a Markdown log in the session's scratchpad, so Claude can report
its method from what really happened instead of from recollection.

Usage (from hooks.json):  python bitacora.py batch | failure
The hook input arrives as JSON on stdin.
"""
import json
import os
import re
import sys
import tempfile
import time

LOG_TOOLS_SKIP = {"TodoWrite", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet"}
SUMMARY_TOOLS = {
    "WebFetch": "resumen escrito por un modelo, no el texto de la página",
    "WebSearch": "lista de resultados con resumen escrito por un modelo",
}


def text_of(resp):
    if resp is None:
        return ""
    if isinstance(resp, str):
        return resp
    if isinstance(resp, list):
        parts = []
        for b in resp:
            if isinstance(b, dict):
                parts.append(b.get("text") or "[" + str(b.get("type", "?")) + "]")
            else:
                parts.append(str(b))
        return "\n".join(parts)
    return json.dumps(resp, ensure_ascii=False)


ERROR_HINTS = re.compile(
    r"returned HTTP [45]\d\d|HTTP [45]\d\d [A-Z]|\b[45]\d\d (Not Found|Forbidden|Too Many Requests|Unauthorized|Internal Server Error|Service Unavailable)"
    r"|^Exit code [1-9]|Traceback \(most recent call last\)|\bError:|rate limit|timed out|requires? approval|permission denied|was denied|not allowed", re.I | re.M)


def looks_failed(body):
    # Only the start of a result says whether the call itself failed; text further
    # down may quote errors from elsewhere (for example, a read of this log).
    head = body[:300]
    m = ERROR_HINTS.search(head)
    return m.group(0) if m else None


def num(n):
    return f"{n:,}".replace(",", ".")


def one_line(s, n):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1] + "…"


def describe_input(tool, inp):
    if not isinstance(inp, dict):
        return one_line(inp, 220)
    for key in ("url", "query", "command", "file_path", "pattern", "prompt"):
        if key in inp:
            val = inp[key]
            if key == "prompt" and tool != "WebFetch":
                continue
            return f"{key}: {one_line(val, 220)}"
    return one_line(json.dumps(inp, ensure_ascii=False), 220)


def paths(data):
    base = data.get("scratchpad_dir") or tempfile.gettempdir()
    sid = (data.get("session_id") or "sin-sesion")[:8]
    return (
        os.path.join(base, f"bitacora-verificar-{sid}.md"),
        os.path.join(base, f"bitacora-verificar-{sid}.resultados.jsonl"),
        os.path.join(base, f"bitacora-verificar-{sid}.estado.json"),
    )


def load_state(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"paso": 0, "lote": 0, "errores": {}, "avisado": False}


def save_state(p, st):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "batch"
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace"))
    except ValueError:
        return
    log_p, res_p, st_p = paths(data)
    st = load_state(st_p)

    if mode == "failure":
        # Remember the exact error so the batch line can mark it.
        st["errores"][data.get("tool_use_id", "")] = one_line(data.get("error", ""), 400)
        save_state(st_p, st)
        return

    calls = data.get("tool_calls") or []
    calls = [c for c in calls if c.get("tool_name") not in LOG_TOOLS_SKIP]
    own = "bitacora-verificar-"
    calls = [c for c in calls if own not in json.dumps(c.get("tool_input") or {}, ensure_ascii=False)]
    if not calls:
        return

    new_file = not os.path.exists(log_p)
    st["lote"] += 1
    hora = time.strftime("%H:%M:%S")
    agente = data.get("agent_type") or ""
    lines = []
    if new_file:
        lines.append("# Bitácora automática (verum)\n")
        lines.append("La escribe un hook después de cada lote de herramientas. Las llamadas del mismo lote salieron juntas: ninguna respondió a otra.\n")
        lines.append("| paso | lote | hora | herramienta | entrada | resultado |")
        lines.append("|---|---|---|---|---|---|")
    with open(res_p, "a", encoding="utf-8") as rf:
        for c in calls:
            st["paso"] += 1
            tool = c.get("tool_name", "?")
            body = text_of(c.get("tool_response"))
            err = st["errores"].pop(c.get("tool_use_id", ""), None)
            hint = None if err is not None else looks_failed(body)
            if err is not None:
                res = f"ERROR: {err}"
            elif hint:
                res = f"POSIBLE ERROR (el resultado dice \"{one_line(hint, 60)}\"), {num(len(body))} caracteres: {one_line(body, 160)}"
            else:
                res = f"OK, {num(len(body))} caracteres"
                if tool in SUMMARY_TOOLS:
                    res += f" ({SUMMARY_TOOLS[tool]})"
                res += f": {one_line(body, 140)}"
            name = tool + (f" [{agente}]" if agente else "")
            lines.append(f"| {st['paso']} | {st['lote']} | {hora} | {name} | {describe_input(tool, c.get('tool_input')).replace('|', '/')} | {res.replace('|', '/')} |")
            rf.write(json.dumps({"paso": st["paso"], "lote": st["lote"], "herramienta": tool,
                                 "entrada": c.get("tool_input"), "error": err, "resultado": body},
                                ensure_ascii=False) + "\n")
    with open(log_p, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    if not st.get("avisado"):
        st["avisado"] = True
        save_state(st_p, st)
        msg = (f"Bitácora automática activa: {log_p} (texto completo de cada resultado en {res_p}). "
               "Un hook anota cada herramienta que usas, con lote, entrada, tamaño del resultado y errores tal cual. "
               "No lleves otra bitácora: cuando describas tu método, léela y escribe desde ella.")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolBatch", "additionalContext": msg}}, ensure_ascii=True))
    else:
        save_state(st_p, st)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # a logging hook must never break the session
        sys.stderr.write(f"bitacora.py: {e}\n")
        sys.exit(0)
