# fin-calc — Help

Welcome to **fin-calc**, a small collection of command-line financial calculators
written in Python. This guide gets you from a fresh checkout to running the tools
and the test suite.

## What's in here

| File | What it does |
| --- | --- |
| `retirement_calculator.py` | Interactive retirement planner. Solve for any one of four variables given the other three. |
| `retirement_calculator.md` | The concept and math behind the retirement calculator. |
| `loan_calculator.py` | Interactive loan calculator — monthly payment, total repaid, total interest. |
| `test_retirement_calculator.py` | Pytest suite covering the retirement solvers. |
| `requirements.txt` | Third-party dependencies (currently none — the calculators use only the standard library). |

## Requirements

- **Python 3.14** (a matching virtual environment already lives in `.venv/`).
- **pytest** — only needed to run the test suite (already installed in `.venv/`).

The calculators themselves depend only on the Python standard library
(`argparse`, `math`), so no installation is required to run them.

## Getting started

Activate the bundled virtual environment:

```bash
source .venv/bin/activate
```

If you'd rather create your own environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest        # only needed for the tests
```

## Running the calculators

### Retirement calculator

```bash
python retirement_calculator.py
```

It prompts you to pick which variable to solve for, then asks for the annual
interest rate and the three known values:

1. **Monthly contribution** — how much to save each month.
2. **Accumulation years** — how many years to save.
3. **Monthly payout** — how much you can draw each month in retirement.
4. **Payout years** — how long the savings last.

The model: you save `monthly_contribution` each month for `accumulation_years`,
earning compound interest monthly. That builds a nest egg, which then pays out
`monthly_payout` each month for `payout_years` (interest keeps compounding during
the payout phase too). Supply any three values and it computes the fourth.

Optional flag to change the currency symbol (default `€`):

```bash
python retirement_calculator.py --currency '$'
```

Example session:

```
=== Retirement Calculator ===

Solve for:
  1. Monthly contribution
  2. Accumulation years
  3. Monthly payout
  4. Payout years

Your choice (1-4): 1
Annual interest rate (%): 6
Accumulation years: 30
Monthly payout (€): 2000
Payout years: 20
```

See `retirement_calculator.md` for the full concept and the formulas used.

### Loan calculator

```bash
python loan_calculator.py
```

Enter the loan amount, annual interest rate (%), and duration in years. It prints
the monthly payment, total repaid, and total interest.

## Running the tests

```bash
pytest
```

or, for the retirement suite specifically:

```bash
pytest test_retirement_calculator.py -v
```

The tests check each solver against known zero-interest results and verify that
the solvers round-trip against each other (e.g. the contribution computed for a
target number of years, fed back in, recovers those same years).

## Notes & edge cases

- A **0% interest rate** is handled everywhere — the math falls back to simple
  division rather than the compound-interest formulas.
- In the retirement calculator, if the chosen monthly payout is small enough that
  interest alone covers it, "Payout years" reports **indefinitely** (the nest egg
  never runs out).
- All inputs are read interactively via prompts; there is no batch/scriptable mode
  yet aside from the `--currency` flag.
