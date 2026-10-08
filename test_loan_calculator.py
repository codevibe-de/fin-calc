import pytest

import loan_calculator
from loan_calculator import amortization_schedule, monthly_payment, yearly


def run_cli(monkeypatch, capsys, answers, argv=()):
    # runs the interactive CLI with canned answers and returns its output lines
    monkeypatch.setattr("sys.argv", ["loan_calculator.py", *argv])
    feed = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(feed))
    loan_calculator.main()
    return capsys.readouterr().out.splitlines()


class TestMonthlyPayment:
    def test_zero_rate(self):
        # no interest: principal split evenly over the months
        assert monthly_payment(10_000, 0, 24) == pytest.approx(10_000 / 24)

    def test_with_rate(self):
        # standard annuity formula at 5% p.a.
        m = 0.05 / 12
        assert monthly_payment(10_000, 5, 24) == pytest.approx(10_000 * m / (1 - (1 + m) ** -24))


class TestAmortizationSchedule:
    def test_zero_rate_two_years(self):
        # spec: 10000 / 0 / 2 years -> 5000 repaid per year, balance 5000 then 0
        years = yearly(amortization_schedule(10_000, 0, 24))
        assert [(y.period, round(y.interest, 2), round(y.principal, 2), round(y.balance, 2)) for y in years] == [
            (1, 0.0, 5000.0, 5000.0),
            (2, 0.0, 5000.0, 0.0),
        ]

    def test_interest_falls_principal_rises(self):
        # spec: with interest, year 1 pays more interest and repays less than year 2
        first, second = yearly(amortization_schedule(10_000, 5, 24))
        assert first.interest > second.interest
        assert first.principal < second.principal

    def test_sums_match_summary(self):
        # spec: totals agree with the summary within 0.01, last balance is exactly zero
        months = 25 * 12
        rows = amortization_schedule(250_000, 3.8, months)
        total_interest = monthly_payment(250_000, 3.8, months) * months - 250_000
        assert sum(r.interest for r in rows) == pytest.approx(total_interest, abs=0.01)
        assert sum(r.principal for r in rows) == pytest.approx(250_000, abs=0.01)
        assert rows[-1].balance == 0.0

    def test_balance_never_negative(self):
        # rounding must never show up as -0.00
        assert all(r.balance >= 0 for r in amortization_schedule(250_000, 3.8, 300))

    def test_partial_last_year(self):
        # spec: 1.5 years = 18 instalments -> year 2 covers months 13 to 18
        years = yearly(amortization_schedule(10_000, 5, 18))
        assert len(years) == 2
        assert years[1].balance == 0.0


class TestCli:
    def test_summary_unchanged_then_yearly_schedule(self, monkeypatch, capsys):
        # spec: summary lines first, as before, then the yearly plan ending at 0.00
        lines = run_cli(monkeypatch, capsys, ["10000", "5", "2"])
        summary = [l for l in lines if l.startswith(("Monthly payment", "Total repaid", "Total interest"))]
        assert summary == [
            "Monthly payment:      438.71",
            "Total repaid:       10529.13",
            "Total interest:       529.13",
        ]
        header = next(i for i, l in enumerate(lines) if l.split()[:1] == ["Year"])
        assert header > lines.index(summary[-1])
        assert len(lines[header + 1:]) == 2
        assert lines[-1].split()[-1] == "0.00"

    def test_monthly_option(self, monkeypatch, capsys):
        # spec: --monthly prints one row per instalment, numbered 1 to 24
        lines = run_cli(monkeypatch, capsys, ["10000", "5", "2"], ["--monthly"])
        header = next(i for i, l in enumerate(lines) if l.split()[:1] == ["Month"])
        periods = [int(l.split()[0]) for l in lines[header + 1:]]
        assert periods == list(range(1, 25))
