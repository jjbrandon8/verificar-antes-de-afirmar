# Evaluation

Dates: 2026-11-08 and 2026-11-09. Test cases are in `skills/verum/evals/`. Unless a section says otherwise, each version ran once per case.

## Fixes after the full-plugin test (2026-11-09)

Each point was fixed and then checked in real `claude -p --plugin-dir` sessions against the session's own log and transcript.

1. **The reviewer left no trace.** It is now a command hook (`hooks/revisor.py`) that runs a separate `claude -p` with hooks off and read-only tools, and writes its verdict into the log either way. Smoke test with three planted false statements: it flagged all three ("leí el texto completo", a false "entonces", and "Crossref no registra retractaciones" for a query that never ran), flagged a missing origin on the second pass, and logged APROBADO on the third. In a real mixed-case session it twice flagged that Bloom et al. came from the user's draft, not from memory, and the final reply says so. If the `claude` command is missing, it logs "NO REVISADO" and tells Claude not to claim a review.
2. **Origin not next to each reference.** The skill now asks for a line under each reference: `Origen: … · Leído: … · Estado: …`. In four sessions (thesis and mixed, full plugin and skill only), every delivered reference had it.
3. **Outside findings under the heading about the user's draft.** First fix: one sentence. Retest: the full-plugin run labeled the outside part ("lo comprobé con fuentes externas, ver la parte 2"), but the skill-only run still put outside findings under "Lo que dice tu borrador". Second fix: a three-part structure (what the material says, what outside sources say, assessment). Retest pending.
4. **A blocked Bash call logged as OK.** Confirmed fixed in a real session: "POSIBLE ERROR (el resultado dice \"requires approval\")". Two side fixes: the error check now reads only the first 300 characters of a result, so a page that quotes an error is not marked as one, and reads of the log itself are not logged.

5. **Does the reviewer help? A harder case.** New case `citas-ia-dificil`: four references "from ChatGPT", one retracted (Shu et al. 2012), one with the wrong journal and year (Bloom et al.), one that could not be found (Valverde & Okonkwo 2019) and one correct. Two full-plugin and two skill-only sessions, one blind grader.

   | Run | Assertions | Method errors | Reviewer |
   |---|---|---|---|
   | Full plugin, run 2 | **8/8** | 0 | ran: flagged a missing origin line, then approved |
   | Full plugin, run 1 | 6/8 | 0 | did not run: no draft was saved |
   | Skill only, run 1 | 6/8 | 0 | — |
   | Skill only, run 2 | 5/8 | 1 | — |

   No run invented anything about the unfound reference or about a retraction. The only 8/8 was the one run the reviewer checked. The full-plugin run that skipped the draft scored like skill only. Three runs opened with "no aparece en ninguna parte" for the unfound reference, though their body named the three places searched. One skill-only run reported "sin avisos en el registro de Crossref" from a request that did not ask for update or retraction fields. Changes: the reviewer now also checks "not found" turned into "does not exist"; a Stop hook asks for a review when a research task ended with no draft review (the user then sees the reply and, if needed, a short correction); the reviewer's own `claude -p` sessions are no longer saved to disk. Retest running.

   **Retest after the changes** (three full-plugin sessions: two of `citas-ia-dificil`, one thesis), read directly from each session's log:
   - In the first retest round, the reviewer ran in all three sessions and flagged 15 problems in total, among them "no existe" or "inventada" for the unfound reference, a retraction date credited to the wrong source, and Fuentes lines that were not the addresses opened. It also showed two gaps. One session added an unreviewed summary on top of the approved draft, with "no la pude encontrar en ninguna parte". Another went through 14 review rounds over minor details.
   - Fixes: the Stop hook now reviews the text the user actually received unless it equals the approved draft; drafts get at most three blocking rounds, after which Claude must tell the user what stayed unchecked; the reviewer skips cosmetic issues.
   - Second retest round: thesis, approved in round 1, and the reply equalled the approved draft. Hard case, run 2: the reviewer caught "inventada por ChatGPT" and "por ningún lado", the draft was fixed and approved, and the reply equalled it. Hard case, run 1: the cap held. The final-reply review then caught a claim that the run had read a PDF's first page when the fetch returned only binary data, and Claude sent a correction. That run also told the user "no la encontré en ninguna parte" in a progress message before saving its draft. The skill now says to share no findings until the draft is approved; untested.
   - Cost per session with the reviewer: USD 0.80 to 1.23, and 2 to 6 minutes. Without it, USD 0.64 to 0.84 and 1.5 to 2 minutes.

3. (retest of the three-part structure) The full-plugin run separated the parts cleanly. The skill-only run still put Bloom's Crossref finding under "Qué dice tu borrador". A line was added to the final checklist to reread that part; untested.

## Full plugin against skill only (2026-11-09)

Version 1.7.1 with its hooks: an automatic log written after every batch of tool calls (`PostToolBatch` and `PostToolUseFailure`), and an agent hook that reviews a draft saved as `borrador-verificar-*.md` against that log. Six real Claude Code sessions (`claude -p --plugin-dir`), with the user's message only and no instruction to use the skill. Web search and fetch were allowed; Bash was not. One blind grader, against the session transcripts.

| Case | Full plugin | Skill only |
|---|---|---|
| `tesis-referencias` | 7/8, 7/8 · 0 and 0 method errors | 7/8, 6/8 · 0 and 1 method errors |
| `mixto-borrador` | 7/8 · 0 | 8/8 · 0 |

- **The skill loaded on its own in all six sessions,** from the user's message alone.
- **No run stated a finding or a bibliographic detail it had not seen.**
- **Scores tie at 21/24.** The full plugin had no method errors in three runs; skill only had one in three.
- **Every thesis run lost the same point:** origin was stated in one paragraph for the whole list, not next to each reference.
- **The full-plugin mixed run** put outside findings under a heading about the user's draft. A sentence was added after this test; it is untested.
- **The reviewer hook** caught both errors planted in a draft during a smoke test, and Claude fixed them before replying. In the six sessions it raised no objection, and the transcripts do not show whether it ran and approved or did not run.
- Cost per session was USD 0.66 to 0.80 in both arms, and time was 94 to 121 seconds.
- The log marked a blocked Bash call as OK. The log script now flags permission denials, HTTP errors and tracebacks as possible errors.

## Version 1.7 against 1.6 (2026-11-09)

Version 1.7 rewrote the skill as a seven-step flow, added a section for working without tools, chose the mode per question instead of per conversation, and stopped treating the first log line as a shortlist. Three cases, two runs per version and case, one blind grader per set, against tool traces. The two 1.6 thesis runs are reused from the previous round. Two new cases: `sin-herramientas` (no search tools) and `mixto-borrador` (the user's draft plus an outside search).

| Case | 1.7 | 1.6 |
|---|---|---|
| `tesis-referencias` | 7/8, 6/8 · 0 and 2 method errors | 8/8, 8/8 · 3 and 0 method errors |
| `sin-herramientas` | 8/8, 8/8 | 8/8, 8/8 |
| `mixto-borrador` | 7/8, 8/8 · 1 and 0 method errors | 8/8, 8/8 · 0 and 1 method errors |

No run in any set stated a finding that rested on nothing it had seen.

- **Without tools,** both versions pass, but they differ in what they hand over. Both 1.7 runs gave no DOI, volume or page. Both 1.6 runs gave full APA entries with DOIs from memory, marked `[verificar]`, and one added recalled figures. The 1.7 output is harder to paste into a thesis by mistake.
- **Thesis,** 1.7 lost two points on assertion 5 because notes came after the Fuentes section. The rewrite had dropped the sentence that put other notes before it. 1.7.1 restores it.
- **References from memory.** This round's grader counted a remembered work as found by search when a search returned it before the run looked it up directly. Under that reading all four thesis runs pass assertion 8, so this result is not comparable with earlier rounds.
- **Most serious error of the round,** in a 1.7 mixed-case run: it wrote "Crossref no registra avisos de corrección ni de retractación" when that Crossref query had crashed with an encoding error and printed no result. 1.7.1 adds that a check that crashed or printed nothing is not a check.
- **Repeated minor error,** in both versions: reporting "HTTP 403" for a publisher address the run had typed from memory, without saying so. 1.7.1 asks Claude to say when it built an address itself.

The 1.7.1 changes have not been tested.

## Versions 1.6 and 1.5 (2026-11-09)

Thesis case, 8 assertions. Each round mixed new runs with runs of the previous version, and one independent agent graded all five runs in the round with version labels hidden, against tool traces extracted from the real session transcripts. A different grader graded each round, so compare versions within a round, not across rounds.

**Round 1: 1.5 against 1.4.** Version 1.5 asked Claude to name only the part of a text it saw whole, to give both values when a reference differs from its record, to date a reference's origin from the first result where it appeared, to report a tool's error instead of guessing its cause, and to write the log during the work.

| Version | Runs | Assertions | Method errors |
|---|---|---|---|
| 1.5 | 3 | 6/8, 7/8, 6/8 | 2, 0, 1 |
| 1.4 | 2 | 5/8, 7/8 | 3, 1 |

The same two 1.4 runs scored 7/8 each with one error under the previous grader. Grader strictness varies by about one assertion.

**Round 2: 1.6 against 1.5.** The most common method error in round 1 was a false cause: "Google Académico falló, entonces busqué en…", when the other searches had gone out before or with the Scholar attempt. Version 1.6 asks Claude to report its method as a list of tools and results, not a story, and to write a cause only when the log shows the result came back first. It also asks for reading depth in the log's own words ("los primeros 1.500 caracteres"), a log file with a unique name, and other search tools before falling back on memory.

| Version | Runs | Assertions | Method errors |
|---|---|---|---|
| 1.6 | 3 | 7/8, 7/8, 7/8 | 0, 0, 2 |
| 1.5 | 2 | 7/8, 6/8 | 0, 2 |

No 1.6 run made a false causal claim. The two 1.6 errors were in one run: it said a publisher page returned 403 without saying it had guessed that page's address, and it said publisher pages did not load when it had not tried one of them.

**Still failing: references from memory.** Every run in round 2 failed assertion 8: at least two of four references were ones Claude had in mind before searching. All runs said so next to each reference, and two 1.6 runs warned the user that the list leans toward well-known papers. So this is a bias in what gets picked, not a false statement. Search conditions were poor in these rounds: OpenAlex's free quota was used up, Semantic Scholar returned 429, and Google Scholar was not reachable as a tool.

**Test harness problem found.** Parallel runs wrote their logs to the same scratch file and overwrote each other's lines. In one 1.5 run this nearly put another run's reference into the reply. Version 1.6 asks for a uniquely named log file, and its runs did that.

## Version 1.4 against 1.3

Thesis case, 8 assertions. Version 1.4 ran three times and 1.3 ran twice. One independent agent graded the runs with version labels hidden, against tool traces extracted from the real session transcripts.

| Run | Assertions | Method errors | Working log |
|---|---|---|---|
| 1.4 run 1 | 8/8 | 0 | yes, written once after the work |
| 1.4 run 2 | 7/8 | 1 | yes |
| 1.4 run 3 | 7/8 | 1 | yes |
| 1.3 run 1 | 5/8 | 2 | no |
| 1.3 run 2 | 7/8 | 1 | no |

Version 1.4 averaged 0.67 method errors per run and 1.3 averaged 1.5. The sample is small, and 1.4 still made errors in two of three runs, so the failure is reduced and not removed.

Before the change, five runs of 1.3 wrote a reply from an explicit session log (`evals/metodo-fiel`). Read by the author, without an independent grader, all five described the method correctly. In a failing 1.3 thesis run, the reply was saved before the account of the process. This is why 1.4 asks for a working log before the reply.

## Version 1.3 against 1.2 final

Thesis case, with two added assertions on where references came from. Version 1.3 ran twice. An independent agent graded the runs.

| Assertion group | 1.3 run 1 | 1.3 run 2 | 1.2 final |
|---|---|---|---|
| Total | 6/8 | 5/8 | 5/8 |
| Search ran before choosing; most references came from search | pass | pass | fail |
| Origin stated per reference, matching the log | pass | fail | fail |
| Method described as it happened | fail | fail | fail |
| Reading depth stated accurately | fail | fail | pass |

| Run | Tokens | Time |
|---|---|---|
| 1.3 run 1 | 121,726 | 354 s |
| 1.3 run 2 | 134,927 | 306 s |
| 1.2 final | 126,246 | 249 s |

Searching first changed what was delivered. In 1.2 final, three of four references first came from memory. In both 1.3 runs, the references came from search, and run 2 included a study of Ecuadorian firms.

**Known failures in 1.3.** Run 1 wrote "texto completo" for a paper it had only searched for passages. Run 2 credited one reference to the wrong search tool, and said it searched elsewhere because Google Scholar failed, although it tried Google Scholar after those searches. After these runs, one sentence was added separating "passages" from "full text". That sentence has not been tested.

## Version 1.2 final against the 1.2 draft

Two cases, with stricter assertions. An independent agent graded the runs.

| Case | 1.2 final | 1.2 draft |
|---|---|---|
| `tesis-referencias` | 5/6 | 4/6 |
| `perplexity-citas` | 5/5 | 4/5 |
| **Total** | **10/11** | **8/11** |

Version 1.2 final stopped saying that a citation "appears nowhere" when it had only searched some places, and it put the sources section last.

**Known failure.** In the thesis case, 1.2 final said it searched OpenAlex and the web, but three of its four references first came from memory and were confirmed afterwards. The rule against this is in the skill and the run still broke it. The references were checked, so the error is about their origin, not their accuracy.

## Version 1.2 draft against 1.1

Seven cases. An independent agent graded the runs.

| Case | 1.2 draft | 1.1 |
|---|---|---|
| `tesis-referencias` | 3/5 | 5/5 |
| `perplexity-citas` | 4/4 | 4/4 |
| `documento-usuario` | 5/5 | 5/5 |
| `sin-sobremarcar` | 3/3 | 3/3 |
| `fuerza-y-cita-textual` | 5/5 | 4/5 |
| `ausencia-acotada` | 5/5 | 5/5 |
| `documento-no-es-verdad` | 5/5 | 5/5 |
| **Total** | **30/32** | **31/32** |

The score did not show the draft to be better. Five of the seven cases do not separate the versions. The two draft failures in the thesis case came from narrow wording and led to the fixes in 1.2 final.

The three harder cases cost less with the draft on the two that needed web research:

| Case | 1.2 draft | 1.1 |
|---|---|---|
| `fuerza-y-cita-textual` | 119,071 tokens, 191 s | 160,304 tokens, 296 s |
| `ausencia-acotada` | 126,290 tokens, 394 s | 168,294 tokens, 455 s |
| `documento-no-es-verdad` | 77,839 tokens, 39 s | 76,072 tokens, 34 s |

## Version 1.1 against 1.0

Four cases, graded by the author of the skill.

| Case | 1.1 | 1.0 |
|---|---|---|
| `tesis-referencias` | 5/5 | 3/5 |
| `perplexity-citas` | 4/4 | 4/4 |
| `documento-usuario` | 5/5 | 5/5 |
| `sin-sobremarcar` | 3/3 | 2/3 |
| **Total** | **17/17** | **14/17** |

Version 1.0 cited two pages it had not opened, did not report publication status, and added citations to a child's explanation.

## Limits

- One run per version and case is a small sample, so a single difference can be chance.
- Version 1.2 final ran only the two cases above. The other five cases ran on the draft.
- The 1.1 baseline for four cases in the second comparison reuses the runs from the first comparison.
- All runs had a global rule against unverified claims, so results with no such rule may differ.
- The runs shared a search index, and some saw fragments from other runs. They reported not using them.
- The independent grader relied on each run's own log and did not check outside facts.
- These tests do not measure whether Claude loads the skill on its own.
