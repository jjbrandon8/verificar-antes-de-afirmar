# verificar-antes-de-afirmar

A Claude plugin so that every fact in an answer shows where it came from, and Claude does not misstate how it found it.

[Español](#español) · [English](#english)

---

## Español

### Qué hace

Para cada pregunta, Claude decide en qué se apoya:

1. **Tus fuentes.** Si le das documentos, enlaces o carpetas y preguntas sobre ellos, responde solo con eso y cita el lugar exacto. Si la respuesta no está ahí, te lo dice.
2. **Fuentes de afuera.** Si no le das nada, busca y abre la fuente original (papers, textos oficiales, documentación) y cita al lado de cada dato. Puede buscar en Google Académico, Perplexity, Scopus, PubMed, SciELO o cualquier otra herramienta; lo que cita es el documento original.
3. **Las dos.** Si le das un documento y le pides algo más (por ejemplo, referencias para tu borrador), separa lo que dice tu material, lo que dicen las fuentes de afuera y su evaluación.

Sirve para cualquier tema. Solo cita lo que abrió, comprueba que la fuente diga ese dato con la misma fuerza y alcance, y que siga vigente (ley reformada, paper retractado, versión vieja). No convierte "no lo encontré" en "no existe". Solo da citas textuales y páginas que vio. En referencias de tesis busca antes de elegir, y debajo de cada referencia pone de dónde salió, cuánto leyó y su estado. Lo que no puede verificar lo marca `[verificar]` o lo deja fuera. **Sin herramientas de búsqueda,** lo dice al principio y no entrega referencias terminadas: a lo sumo candidatos "de memoria, sin verificar", sin DOI ni páginas inventadas.

En textos para enviar (propuestas, informes, correos, tesis), cada dato lleva su número `[1]` y el texto termina con su sección de Fuentes, para que la evidencia viaje con lo que copias.

### Bitácora y revisor automáticos (cowork y Claude Code)

El plugin trae además dos hooks que funcionan donde corren los hooks (cowork y Claude Code; el chat de claude.ai los ignora):

- **Bitácora automática.** Después de cada lote de herramientas, un script anota cada búsqueda y lectura: qué pidió, cuántos caracteres volvieron, si fue un resumen escrito por un modelo y el error tal cual. Las llamadas que salieron juntas quedan en el mismo lote. Claude cuenta su método desde ahí, no de memoria.
- **Revisor.** En tareas de investigación, Claude guarda un borrador y un segundo Claude lo compara con la bitácora antes de que te llegue: fuentes que dice haber abierto, cuánto leyó, verificaciones que fallaron, "no existe" sin prueba, causas inventadas. Como máximo hace tres rondas. Al terminar, revisa también lo que de verdad te llegó; si encuentra algo, Claude te manda una corrección breve. Cada veredicto queda anotado en la bitácora.

Requisitos: `python` en el PATH para los dos hooks, y el comando `claude` para el revisor. Si falta `claude`, el revisor anota "NO REVISADO" y Claude no puede decir que hubo revisión. Costo medido: con el revisor, una tarea de referencias costó entre USD 0,80 y 1,23 y tardó de 2 a 6 minutos; sin él, entre USD 0,64 y 0,84 y de 1,5 a 2 minutos.

### Pruebas

La comparación entre versiones, con sus resultados y límites, está en [EVALS.md](EVALS.md).

### Instalar

**claude.ai, cowork y Claude Code a la vez:** en [Customize > Plugins](https://claude.ai/customize/plugins), elige **Add > Add marketplace**, escribe `jjbrandon8/verificar-antes-de-afirmar` e instala `verificar-antes-de-afirmar`. Activa **Sync automatically** para recibir las versiones nuevas. Si antes subiste la skill como `.zip` en Customize > Skills, bórrala, para no tener dos copias.

**Solo Claude Code:**

```
/plugin marketplace add jjbrandon8/verificar-antes-de-afirmar
/plugin install verificar-antes-de-afirmar@jjbrandon8-verificar
```

Una skill se carga cuando Claude decide que aplica (en las pruebas se cargó sola en todas las sesiones). Para reforzarlo, agrega esto a tu `~/.claude/CLAUDE.md` y a tus instrucciones personales de claude.ai:

```markdown
## No inventar

Antes de afirmar un dato, cifra, fecha, ley, artículo, cita, enlace, versión o resultado, usa la skill `verificar-antes-de-afirmar`:
- Si el usuario dio fuentes, responde solo con ellas y cita el lugar exacto. Si no está ahí, dilo.
- Si no dio fuentes, busca en todo lo que sirva (Google Académico, Perplexity, bases de datos u otros) y abre el documento original antes de citarlo.
- Lo que no puedas verificar se marca `[verificar]` o se deja fuera. La memoria no es una fuente.
```

---

## English

### What it does

For each question, Claude decides what it rests on:

1. **Your sources.** If you give it documents, links or folders and ask about them, it answers only from them and cites the exact place. If the answer is not there, it says so.
2. **Outside sources.** If you give none, it finds and opens the original source (papers, official texts, documentation) and cites next to each fact. It can search Google Scholar, Perplexity, Scopus, PubMed, SciELO or any other tool; what it cites is the original document.
3. **Both.** If you give a document and ask for more (for example, references for your draft), it separates what your material says, what outside sources say, and its assessment.

It works on any topic. It cites only what it opened, and checks that the source says that fact at the same strength and scope and still holds (amended law, retracted paper, old version). It does not turn "not found" into "does not exist". It gives only quotes and page numbers it saw. For thesis references it searches before choosing, and under each reference it states where it came from, how much it read and its status. What it cannot verify is marked `[verify]`, or left out. **Without search tools,** it says so first and delivers no finished references: at most candidates "from memory, unverified", with no invented DOI or pages.

In text meant to be sent (proposals, reports, emails, theses), each fact gets a number `[1]` and the text ends with its own Sources section, so the evidence travels with what you copy.

### Automatic log and reviewer (Cowork and Claude Code)

The plugin also ships two hooks, which work wherever hooks run (Cowork and Claude Code; claude.ai chat ignores them):

- **Automatic log.** After each batch of tool calls, a script records every search and read: what was asked, how many characters came back, whether it was a model-written summary, and the error as given. Calls sent together share a batch number. Claude reports its method from this log, not from recollection.
- **Reviewer.** On research tasks, Claude saves a draft and a second Claude checks it against the log before you see it: sources it claims to have opened, how much it read, checks that failed, "does not exist" without proof, invented causes. It runs at most three rounds. At the end it also checks what you actually received; if something is off, Claude sends a short correction. Every verdict is written into the log.

Requirements: `python` on the PATH for both hooks, and the `claude` command for the reviewer. If `claude` is missing, the reviewer logs "NO REVISADO" and Claude may not claim a review. Measured cost: with the reviewer, a references task cost USD 0.80 to 1.23 and took 2 to 6 minutes; without it, USD 0.64 to 0.84 and 1.5 to 2 minutes.

The comparison between versions is in [EVALS.md](EVALS.md).

### Install

**claude.ai, Cowork and Claude Code at once:** in [Customize > Plugins](https://claude.ai/customize/plugins), choose **Add > Add marketplace**, enter `jjbrandon8/verificar-antes-de-afirmar` and install `verificar-antes-de-afirmar`. Turn on **Sync automatically** to get new versions. If you uploaded the skill as a `.zip` in Customize > Skills before, delete it so you do not have two copies.

**Claude Code only:**

```
/plugin marketplace add jjbrandon8/verificar-antes-de-afirmar
/plugin install verificar-antes-de-afirmar@jjbrandon8-verificar
```

A skill loads when Claude decides it applies (in testing it loaded on its own in every session). To reinforce it, add the rule block shown in the Spanish section to your `~/.claude/CLAUDE.md` and your claude.ai personal instructions.

## License

MIT
