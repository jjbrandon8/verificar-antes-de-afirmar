# Evaluation

Dates: 2026-11-08 and 2026-11-09. Test cases are in `skills/verificar-antes-de-afirmar/evals/`. Unless a section says otherwise, each version ran once per case.

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
