# Reflection

The handout describes the learning outcomes but does not include four
numbered reflection questions. These answers address four reflection prompts
based on those outcomes.

## 1. What did static analysis contribute to this lab?

Pylint, Flake8, and Bandit found different kinds of problems without running
the program. Pylint highlighted maintainability issues such as missing
docstrings, a mutable default argument, and unused variables. Flake8 found
formatting and Python-style violations. Bandit identified unsafe patterns
including `eval`, weak hashing, shell execution, and non-cryptographic
randomness. Using all three gave a broader view than relying on one tool.

## 2. Which findings were most important, and how were they addressed?

The most important findings were the shell command and dynamic `eval`, because
both could turn input into unintended command or code execution. The code now
writes the manifest directly and computes the baggage fee from a validated
numeric rate. I also replaced MD5, used a secure random source for the PIN,
removed the hard-coded token, and eliminated the mutable list default and
silent exception handling.

## 3. What did static analysis not catch, and how did you verify behavior?

Static analysis did not establish that the reservation logic behaved
correctly. In particular, repeated cancellations could increase the number of
available seats beyond flight capacity. I added capacity checks and ran
functional checks for booking, availability, cancellation limits, fee
validation, hash/PIN generation, and manifest export. I also ran the sample
program and confirmed its expected output.

## 4. How will you use static analysis in future work?

I would run style, quality, and security checks regularly—ideally as part of
automated tests or continuous integration—and review each finding rather than
blindly suppressing it. I would also pair static analysis with tests and code
review, since no single tool can prove that a program is correct or secure.
