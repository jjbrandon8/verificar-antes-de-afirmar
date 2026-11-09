# verificar-antes-de-afirmar

A Claude skill so that every fact in an answer shows where it came from.

[Español](#español) · [English](#english)

---

## Español

### Qué hace

Claude trabaja en uno de dos modos:

1. **Con tus fuentes.** Si le das documentos, enlaces o carpetas, responde solo con eso y cita el lugar exacto. Si la respuesta no está ahí, te lo dice.
2. **Con fuentes válidas.** Si no le das nada, busca y abre la fuente original (papers, textos oficiales, documentación) y cita al lado de cada dato. Puede buscar en Google Académico, Perplexity, Scopus, PubMed, SciELO o cualquier otra herramienta; lo que cita es el documento original.

Sirve para cualquier tema. Solo cita lo que abrió, comprueba que la fuente diga ese dato con la misma fuerza y alcance, y que siga vigente (ley reformada, paper retractado, versión vieja). No convierte "no lo encontré" en "no existe". Solo da citas textuales y páginas que vio. En referencias de tesis busca antes de elegir, dice de dónde salió cada una, confirma que existan, dice cuánto leyó y avisa de retractaciones y preprints. Lo que no puede verificar lo marca `[verificar]` o lo deja fuera. El conocimiento común, el razonamiento y la opinión no llevan cita.

Tampoco inventa sobre su propio trabajo. En tareas largas lleva una bitácora paso a paso mientras trabaja, y lo que dice sobre cómo buscó, cuánto leyó o por qué falló una herramienta sale de esa bitácora, no de lo que recuerda.

En textos para enviar (propuestas, informes, correos, tesis), cada dato lleva su número `[1]` y el texto termina con su sección de Fuentes, para que la evidencia viaje con lo que copias.

### Pruebas

La comparación entre versiones, con sus resultados y límites, está en [EVALS.md](EVALS.md).

### Instalar

**Claude Code:**

```
/plugin marketplace add jjbrandon8/verificar-antes-de-afirmar
/plugin install verificar-antes-de-afirmar@jjbrandon8-verificar
```

Una skill se carga solo cuando Claude decide que aplica. Para que se use siempre, agrega esto a tu `~/.claude/CLAUDE.md`:

```markdown
## No inventar

Antes de afirmar un dato, cifra, fecha, ley, artículo, cita, enlace, versión o resultado, usa la skill `verificar-antes-de-afirmar`:
- Si el usuario dio fuentes, responde solo con ellas y cita el lugar exacto. Si no está ahí, dilo.
- Si no dio fuentes, busca en todo lo que sirva (Google Académico, Perplexity, bases de datos u otros) y abre el documento original antes de citarlo.
- Lo que no puedas verificar se marca `[verificar]` o se deja fuera. La memoria no es una fuente.
```

**claude.ai:** comprime la carpeta `skills/verificar-antes-de-afirmar` en un `.zip`, sin la subcarpeta `evals` (son pruebas, no hacen falta para usarla), y súbela en [Customize > Skills](https://claude.ai/customize/skills). Pega también el bloque de arriba en tus instrucciones personales.

---

## English

### What it does

Claude works in one of two modes:

1. **Your sources.** If you give it documents, links or folders, it answers only from them and cites the exact place. If the answer is not there, it says so.
2. **Valid sources.** If you give none, it finds and opens the original source (papers, official texts, documentation) and cites next to each fact. It can search Google Scholar, Perplexity, Scopus, PubMed, SciELO or any other tool; what it cites is the original document.

It works on any topic. It cites only what it opened, and checks that the source says that fact at the same strength and scope and still holds (amended law, retracted paper, old version). It does not turn "not found" into "does not exist". It gives only quotes and page numbers it saw. For thesis references it searches before choosing, says where each one came from, confirms they exist, says how much it read, and flags retractions and preprints. What it cannot verify is marked `[verify]`, or left out. Common knowledge, reasoning and opinion need no citation.

It does not make things up about its own work either. On long tasks it keeps a step-by-step log as it works, and what it says about how it searched, how much it read or why a tool failed comes from that log, not from recollection.

In text meant to be sent (proposals, reports, emails, theses), each fact gets a number `[1]` and the text ends with its own Sources section, so the evidence travels with what you copy. The comparison between versions is in [EVALS.md](EVALS.md).

### Install

**Claude Code:**

```
/plugin marketplace add jjbrandon8/verificar-antes-de-afirmar
/plugin install verificar-antes-de-afirmar@jjbrandon8-verificar
```

A skill loads only when Claude decides it applies. To have it used every time, add the rule block shown in the Spanish section to your `~/.claude/CLAUDE.md`.

**claude.ai:** zip the `skills/verificar-antes-de-afirmar` folder, leaving out the `evals` subfolder (tests, not needed to use it), and upload it in [Customize > Skills](https://claude.ai/customize/skills). Paste the same rule into your personal instructions.

## License

MIT
