"""Reviewer for the verum plugin (verificar antes de afirmar).

Two entry points, both called from hooks.json:

  python revisor.py        PostToolUse on Write/Edit of borrador-verificar-*.md.
                           Reviews the draft against the automatic log before
                           Claude replies. At most MAX_ROUNDS blocking rounds.
  python revisor.py stop   Stop. Reviews what the user actually received, unless
                           it is exactly the approved draft. If there are
                           problems, Claude sends a short correction.

The review itself runs in a separate `claude -p` with hooks off, read-only tools
and no saved session. Every verdict is written into the log, including failures,
so nobody can claim a review that did not happen.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bitacora import paths, one_line  # noqa: E402

MAX_ROUNDS = 3
RESEARCH_TOOLS = ("| WebSearch", "| WebFetch", "| Bash", "| mcp__")

REVIEW_PROMPT = """You review a reply against the automatic tool log of the session that wrote it. Check only these, nothing about style:
1. Every URL, DOI or record the reply cites as read or opened appears in the log with an OK result. A source that appears only inside a search result list was not opened.
2. Every statement of how much was read matches the log. WebFetch and WebSearch return a model-written summary, not the page. A short result cannot be "el texto completo"; a cut result cannot be "el resumen completo".
3. Every check the reply reports as clean (no retraction, no correction, matches the record) has an OK log line that shows it. A line marked ERROR or POSIBLE ERROR is not a check.
4. Every tool error the reply mentions matches the log's text, and the reply names no cause the error does not state.
5. No sentence says one step happened because of another ("entonces", "así que", "como falló") when both are in the same lote.
6. Every statement of where a reference first appeared matches the first log line whose result contains it.
7. Each academic reference has its origin stated next to it, not only in a general paragraph.
8. The Fuentes (or Sources) section is the last section, and each source line gives an address the log shows was opened (the same resource; extra query parameters do not matter).
9. Nothing not found is called nonexistent: no "no existe", "en ninguna parte", "no aparece en ningún lado" or "inventada", in the first sentence or anywhere, unless the reply names an authoritative record that settles it. "No lo encontré en X, Y y Z" is fine.

The full text of every tool result is in {results} (one JSON object per line, field "resultado"). Use Grep or Read on it when a log line is not enough.

LOG ({log}):
{log_text}

REPLY ({label}):
{text}

Report only problems that change what a reader would believe about the sources or the method; skip cosmetic ones. Answer with one JSON object and nothing else: {{"ok": true}} if all hold, or {{"ok": false, "problems": ["<sentence> -> log step N -> <correction>", ...]}}."""


def state_path(log_p):
    return log_p[:-3] + ".revisor.json"


def load_state(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"rondas": {}, "aprobado_texto": ""}


def save_state(p, st):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False)


def append_log(log_p, verdict, what="REVISOR (revisa la escritura anotada en la línea siguiente)"):
    line = f"| — | — | {time.strftime('%H:%M:%S')} | {what} | {verdict.replace('|', '/')} |"
    with open(log_p, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def emit(obj):
    print(json.dumps(obj, ensure_ascii=True))


def review(text, label, log_p, res_p):
    """Run the separate reviewer. Returns (ok, problems). Raises on failure."""
    exe = shutil.which("claude")
    if not exe:
        raise RuntimeError("no se encontró el comando claude")
    with open(log_p, encoding="utf-8") as f:
        log_text = f.read()
    prompt = REVIEW_PROMPT.format(results=res_p, log=log_p, log_text=log_text[-60000:], label=label, text=text)
    out = subprocess.run(
        [exe, "-p", "--no-session-persistence", "--model", "sonnet",
         "--settings", '{"disableAllHooks": true}',
         "--allowedTools", "Read", "Grep", "Glob", "--output-format", "json"],
        input=prompt.encode("utf-8"), capture_output=True, timeout=280,
    )
    result = json.loads(out.stdout.decode("utf-8", errors="replace")).get("result", "")
    m = re.search(r"\{.*\}", result, re.S)
    if not m:
        raise RuntimeError("respuesta del revisor ilegible")
    verdict = json.loads(m.group(0))
    if verdict.get("ok") is True:
        return True, []
    return False, verdict.get("problems") or [verdict.get("reason", "sin detalle")]


def norm_lines(text):
    return {" ".join(l.split()) for l in text.splitlines() if len(l.split()) > 3}


def draft_check(data):
    draft = (data.get("tool_input") or {}).get("file_path", "")
    name = os.path.basename(draft)
    if not name.startswith("borrador-verificar"):
        return
    log_p, res_p, _ = paths(data)
    if not os.path.exists(log_p):
        return
    with open(draft, encoding="utf-8") as f:
        draft_text = f.read()
    sp = state_path(log_p)
    st = load_state(sp)
    st["rondas"][name] = st["rondas"].get(name, 0) + 1
    rnd = st["rondas"][name]
    save_state(sp, st)
    try:
        ok, problems = review(draft_text, draft, log_p, res_p)
    except Exception as e:  # report, never pretend the review happened
        append_log(log_p, f"borrador {name} / NO REVISADO: {one_line(e, 200)}")
        emit({"hookSpecificOutput": {"hookEventName": "PostToolUse",
              "additionalContext": f"El revisor del borrador falló ({one_line(e, 200)}). El borrador no fue revisado: no digas que lo fue."}})
        return
    if ok:
        st = load_state(sp)
        st["aprobado_texto"] = draft_text
        save_state(sp, st)
        append_log(log_p, f"borrador {name} / APROBADO (ronda {rnd})")
        emit({"hookSpecificOutput": {"hookEventName": "PostToolUse",
              "additionalContext": "Revisor del borrador: sin observaciones. Envía este texto tal cual. Si agregas o cambias algo, se revisará lo que envíes."}})
        return
    joined = "\n- ".join(problems)
    if rnd >= MAX_ROUNDS:
        append_log(log_p, f"borrador {name} / LÍMITE DE {MAX_ROUNDS} RONDAS, quedan observaciones: " + one_line(" ; ".join(problems), 700))
        emit({"hookSpecificOutput": {"hookEventName": "PostToolUse",
              "additionalContext": (f"El revisor llegó al límite de {MAX_ROUNDS} rondas. Corrige lo que puedas y, si queda algo, "
                                    "dile al usuario en una línea qué no quedó comprobado:\n- " + joined)}})
        return
    append_log(log_p, f"borrador {name} / OBSERVACIONES (ronda {rnd} de {MAX_ROUNDS}): " + one_line(" ; ".join(problems), 900))
    emit({"decision": "block",
          "reason": ("El revisor encontró diferencias entre el borrador y la bitácora. Corrige el borrador, guárdalo de nuevo "
                     "con el mismo nombre y luego responde. Atiende lo que cambia lo que el usuario entiende; no hace falta "
                     "pulir detalles de formato.\n- " + joined)})


def stop_check(data):
    if data.get("stop_hook_active"):
        return
    log_p, res_p, _ = paths(data)
    if not os.path.exists(log_p):
        return
    with open(log_p, encoding="utf-8") as f:
        lines = f.readlines()
    if sum(1 for l in lines if any(t in l for t in RESEARCH_TOOLS)) < 3:
        return
    sent = data.get("last_assistant_message") or ""
    approved = load_state(state_path(log_p)).get("aprobado_texto", "")
    if approved and not (norm_lines(sent) - norm_lines(approved)):
        append_log(log_p, "respuesta enviada = borrador aprobado", "REVISOR (respuesta final)")
        return
    try:
        ok, problems = review(sent, "respuesta enviada al usuario", log_p, res_p)
    except Exception as e:
        append_log(log_p, f"NO REVISADA: {one_line(e, 200)}", "REVISOR (respuesta final)")
        return
    if ok:
        note = " (incluye texto que no estaba en el borrador)" if approved else " (no hubo borrador)"
        append_log(log_p, "APROBADA" + note, "REVISOR (respuesta final)")
        return
    append_log(log_p, "OBSERVACIONES: " + one_line(" ; ".join(problems), 900), "REVISOR (respuesta final)")
    emit({"decision": "block",
          "reason": ("El revisor comparó lo que acabas de enviar con la bitácora y encontró diferencias. Envía al usuario "
                     "una corrección breve: qué frase cambia y por qué, sin repetir toda la respuesta.\n- " + "\n- ".join(problems))})


def main():
    data = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace"))
    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        stop_check(data)
    else:
        draft_check(data)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(f"revisor.py: {e}\n")
        sys.exit(0)
