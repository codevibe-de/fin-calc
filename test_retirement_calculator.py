import math
import pytest

from retirement_calculator import (
    _accumulated_savings,
    _required_nest_egg,
    solve_accumulation_years,
    solve_monthly_contribution,
    solve_monthly_payout,
    solve_payout_years,
)


# --- helpers ---

class TestAccumulatedSavings:
    def test_zero_rate(self):
        # no interest: result is simply contribution * months
        assert _accumulated_savings(100, 120, 0) == pytest.approx(12_000)

    def test_with_rate(self):
        # 1% monthly, 12 months, 100/month
        result = _accumulated_savings(100, 12, 0.01)
        assert result == pytest.approx(100 * ((1.01**12 - 1) / 0.01))


class TestRequiredNestEgg:
    def test_zero_rate(self):
        # no interest: nest egg equals payout * months
        assert _required_nest_egg(1_000, 240, 0) == pytest.approx(240_000)

    def test_with_rate(self):
        # verify present-value annuity formula
        result = _required_nest_egg(1_000, 240, 0.005)
        assert result == pytest.approx(1_000 * (1 - 1.005**-240) / 0.005)


# --- solvers ---

class TestSolveMonthlyContribution:
    def test_zero_rate(self):
        # 0% rate: nest egg = 1000 * 240 = 240_000, contribution = 240_000 / 120
        contribution, fv = solve_monthly_contribution(0, 10, 1_000, 20)
        assert fv == pytest.approx(240_000)
        assert contribution == pytest.approx(2_000)

    def test_with_rate(self):
        # accumulating the computed contribution must reproduce the target nest egg
        contribution, fv = solve_monthly_contribution(0.06, 30, 2_000, 20)
        m = 0.06 / 12
        k = 20 * 12
        expected_fv = _required_nest_egg(2_000, k, m)
        assert fv == pytest.approx(expected_fv)
        assert contribution > 0
        # verify: accumulating the computed contribution should reproduce fv
        n = 30 * 12
        assert _accumulated_savings(contribution, n, m) == pytest.approx(fv, rel=1e-6)


class TestSolveAccumulationYears:
    def test_zero_rate(self):
        # 0% rate: years = nest_egg / (contribution * 12)
        years, fv = solve_accumulation_years(0, 2_000, 1_000, 20)
        assert fv == pytest.approx(240_000)
        assert years == pytest.approx(10)

    def test_with_rate(self):
        # round-trip: contribution from solve_monthly_contribution should recover the same years
        rate = 0.06
        target_years = 30.0
        monthly_payout = 2_000
        payout_years = 20
        contribution, fv = solve_monthly_contribution(rate, target_years, monthly_payout, payout_years)
        years, fv2 = solve_accumulation_years(rate, contribution, monthly_payout, payout_years)
        assert years == pytest.approx(target_years, rel=1e-6)
        assert fv2 == pytest.approx(fv, rel=1e-6)


class TestSolveMonthlyPayout:
    def test_zero_rate(self):
        # 0% rate: payout = nest_egg / payout_months
        payout, fv = solve_monthly_payout(0, 2_000, 10, 20)
        assert fv == pytest.approx(240_000)
        assert payout == pytest.approx(1_000)

    def test_with_rate(self):
        # required nest egg for computed payout must equal accumulated savings
        rate = 0.06
        acc_years = 30
        payout_years = 20
        contribution = 500
        payout, fv = solve_monthly_payout(rate, contribution, acc_years, payout_years)
        m = rate / 12
        n = acc_years * 12
        assert fv == pytest.approx(_accumulated_savings(contribution, n, m))
        assert payout > 0
        # verify: required nest egg for computed payout should equal fv
        k = payout_years * 12
        assert _required_nest_egg(payout, k, m) == pytest.approx(fv, rel=1e-6)


class TestSolvePayoutYears:
    def test_zero_rate(self):
        # 0% rate: years = nest_egg / (payout * 12)
        years, fv = solve_payout_years(0, 2_000, 10, 1_000)
        assert fv == pytest.approx(240_000)
        assert years == pytest.approx(20)

    def test_with_rate(self):
        # payout must exceed fv*m (perpetuity threshold) for a finite result
        rate = 0.06
        acc_years = 30
        contribution = 500
        m = rate / 12
        n = acc_years * 12
        fv = _accumulated_savings(contribution, n, m)
        # payout must exceed fv*m (perpetuity threshold) for a finite result
        monthly_payout = fv * m * 2
        years, fv2 = solve_payout_years(rate, contribution, acc_years, monthly_payout)
        assert fv2 == pytest.approx(fv)
        assert years > 0 and not math.isinf(years)

    def test_indefinite_payout(self):
        # payout <= fv * m means interest covers it forever
        rate = 0.06
        m = rate / 12
        contribution = 10_000
        acc_years = 30
        n = acc_years * 12
        fv = _accumulated_savings(contribution, n, m)
        # set payout just below the perpetuity threshold
        perpetuity_payout = fv * m
        years, _ = solve_payout_years(rate, contribution, acc_years, perpetuity_payout * 0.99)
        assert math.isinf(years)

    def test_round_trip_with_monthly_payout_solver(self):
        # recovered payout years must match the original payout_years input
        rate = 0.06
        acc_years = 30
        payout_years = 20
        contribution = 500
        payout, fv = solve_monthly_payout(rate, contribution, acc_years, payout_years)
        recovered_years, fv2 = solve_payout_years(rate, contribution, acc_years, payout)
        assert recovered_years == pytest.approx(payout_years, rel=1e-6)
        assert fv2 == pytest.approx(fv, rel=1e-6)
