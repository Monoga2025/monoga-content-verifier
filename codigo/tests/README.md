# codigo/tests

Test runner and fixtures for the verifier.

- `run_tests.py`: runs the 90 checks (one valid fixture plus invalid fixtures, one per rule). Expected result: 90/90.
- `fixtures/`: the pieces and contexts used by the checks.
- `run_tests.py` is run from the repo root with `python codigo/tests/run_tests.py`.
