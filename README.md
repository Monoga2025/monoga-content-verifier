# Content Verifier

A rule-based **verifier** (not a generator) for short-form video scripts. It refuses to let content through unless the brand context is complete and every claim in a piece is backed by that context. Pure Python standard library, no dependencies.

## What it does

| Script | Purpose |
|---|---|
| `codigo/validar_contexto.py` | Checks the brand-context file has all 11 mandatory fields; if one is missing it blocks generation and names it. |
| `codigo/validar_pieza.py` | Checks a script against 19 rules: hook length, five distinct hooks/triggers, four labelled layers, single CTA, declared framework, sensitive-topic review, and **no unsupported figures or superlatives** (e.g. "2000 euros" not found in the context is rejected). |
| `codigo/derivar_indice.py` | Regenerates the content-bank index from the pieces themselves. |
| `codigo/verificar_reglas.py` | Checks that the rule documents don't contradict each other. |
| `codigo/tests/run_tests.py` | 90 checks: one valid fixture plus invalid fixtures, one per rule. |

Approving, publishing or discarding a piece is deliberately human-only: the tool never changes a piece's state.

## Run

```bash
python codigo/tests/run_tests.py          # expect: 90/90
python codigo/validar_contexto.py --archivo marca/contexto-marca.md
python codigo/validar_pieza.py <piece.md>
```

The real brand-context file is private and not included; the test fixtures under `codigo/tests/fixtures/` exercise every rule.

## Structure

```
codigo/        validators + tests + fixtures
reglas/        business and style rules (BR-001..BR-012), AIDA, triggers, taxonomy
docs/product/  product docs: brief, scope, domain model, flows, architecture, build plan
banco/         generated index of the content bank
```

## Status

🟢 Verifier works (90/90 tests pass on the staged copy). Known blind spot, documented in the product docs: a promise with no figure and no listed superlative ("you'll sell more") can pass. It does not check audio or video, and it does not generate scripts. Docs and rules are in Spanish.

## Folder guide

| Folder | What it holds |
|---|---|
| [banco/](banco/README.md) | Content bank and its generated index |
| [banco/piezas/](banco/piezas/README.md) | Piece files checked by the validators (empty in this copy) |
| [codigo/](codigo/README.md) | Validators and the rules checker |
| [codigo/tests/](codigo/tests/README.md) | 90-check test runner and fixtures |
| [design-reference/](design-reference/README.md) | Approved design references |
| [docs/](docs/README.md) | Product documentation |
| [docs/product/](docs/product/README.md) | Brief, scope, domain model, build plan and handoff |
| [reglas/](reglas/README.md) | Business and style rules shared by the agent and the verifier |

---

Built by Monoga · [github.com/Monoga2025](https://github.com/Monoga2025)
