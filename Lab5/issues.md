# Static Analysis Findings

The line numbers below refer to the original `flight_reservation_system.py`.
High- and medium-severity findings are listed first.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Weak MD5 passenger hash (Bandit B324) | Security — High | 52 | MD5 is unsuitable for security-sensitive hashing. | Replaced MD5 with SHA-256. A plain hash is still not appropriate for password storage or anonymizing predictable IDs. |
| Shell command built with a filename (Bandit B605) | Security — High | 63 | `os.system` invokes a shell and appends the filename to a command. | Removed shell execution; write the manifest directly and print a status message. |
| Dynamic expression evaluation (Bandit B307, Pylint W0123) | Security — Medium | 45–48 | `eval` executes an expression string to calculate a numeric fee. | Accept a numeric surcharge rate and calculate the fee directly, validating the flight and rate. |
| Mutable default argument (Pylint W0102) | Bug — Medium | 15 | The default list is shared between calls. | Use `None` as the default and create a fresh list within the call. |
| Swallowed exception (Bandit B110, Pylint W0702, Flake8 E722) | Reliability — Low | 27–32 | A bare `except` and `pass` hide errors, including invalid flight numbers. | Replace exception-driven control flow with explicit flight/capacity checks and a boolean result. |
| Predictable boarding PIN (Bandit B311) | Security — Low | 55–56 | `random.randint` is not intended for security-sensitive values. | Use `secrets.randbelow` to generate a four-digit PIN. |
| Hard-coded API token (Bandit B105) | Security — Low | 75 | A secret-like token is embedded in the code and printed. | Removed the token; the demo no longer includes or prints a credential. |
| Cancellation can exceed seat capacity | Logic bug | 27–32 | Repeated cancellations can increase the seat count beyond the flight's actual capacity. | Track each flight's capacity and reject cancellations when already at capacity. |
| Unused variables/import and comparison to `None` (Pylint, Flake8) | Quality/style | 4, 36–37, 46 | Unused `math`, `airport_fee`, and `base_fare` plus `== None` caused analyzer findings. | Removed unused code, used `is None` checks where applicable, and used `math` to validate surcharge rates. |
| Naming, documentation, and formatting findings (Pylint, Flake8) | Quality/style | 1–87 | Missing docstrings, camelCase names, long lines, old-style string formatting, and implicit file encoding reduced readability and lint scores. | Added docstrings, switched functions to `snake_case` and f-strings, wrapped long lines, and used an encoding-aware context manager for file output. |

## Verification

- Bandit: no issues identified.
- Flake8: no findings.
- Pylint: 9.82/10, above the handout's 9.5 target. Its remaining warning is the `global` statement used to update accumulated revenue.
- Functional checks covered booking, cancellation limits, fee validation, hash/PIN generation, manifest export, and the demonstration program.
