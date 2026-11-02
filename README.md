# verificar-antes-de-afirmar

A Claude skill so that every fact in an answer shows where it came from.

[Español](#español) · [English](#english)

---

## Español

### Qué hace

Claude trabaja en uno de dos modos:

1. **Con tus fuentes.** Si le das documentos, enlaces o carpetas, responde solo con eso y cita el lugar exacto. Si la respuesta no está ahí, te lo dice.
2. **Con fuentes válidas.** Si no le das nada, busca en fuentes primarias (textos oficiales, normas, papers, documentación) y cita al lado de cada dato.

Lo que no puede verificar lo marca `[verificar]` o lo deja fuera. En textos para enviar (propuestas, informes, correos), cada dato lleva su número `[1]` y el texto termina con su sección de Fuentes, para que la evidencia viaje con lo que copias.

### Por qué existe

En pruebas sin la skill, Claude respondía bien preguntas directas, pero en textos largos metía datos de memoria (leyes, plazos, conteos, estadísticas) sin fuente, con la advertencia al final. Con la skill, las mismas propuestas salieron con cada dato referenciado y con una lista de Fuentes, y las preguntas fuera de un documento recibieron "no está en las fuentes que me diste".

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
- Si no dio fuentes, verifica en fuentes primarias y cita al lado de cada dato.
- Lo que no puedas verificar se marca `[verificar]` o se deja fuera. La memoria no es una fuente.
```

**claude.ai:** comprime la carpeta `skills/verificar-antes-de-afirmar` en un `.zip` y súbela en [Customize > Skills](https://claude.ai/customize/skills). Pega también el bloque de arriba en tus instrucciones personales.

---

## English

### What it does

Claude works in one of two modes:

1. **Your sources.** If you give it documents, links or folders, it answers only from them and cites the exact place. If the answer is not there, it says so.
2. **Valid sources.** If you give none, it looks facts up in primary sources (official texts, regulations, papers, documentation) and cites next to each fact.

What it cannot verify is marked `[verificar]` / unverified, or left out. In text meant to be sent (proposals, reports, emails), each fact gets a number `[1]` and the text ends with its own Sources section, so the evidence travels with what you copy.

### Install

**Claude Code:**

```
/plugin marketplace add jjbrandon8/verificar-antes-de-afirmar
/plugin install verificar-antes-de-afirmar@jjbrandon8-verificar
```

A skill loads only when Claude decides it applies. To have it used every time, add the rule block shown in the Spanish section to your `~/.claude/CLAUDE.md`.

**claude.ai:** zip the `skills/verificar-antes-de-afirmar` folder and upload it in [Customize > Skills](https://claude.ai/customize/skills). Paste the same rule into your personal instructions.

## License

MIT
