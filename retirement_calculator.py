import argparse
import math


def _fmt(amount: float, currency: str) -> str:
    return f"{amount:>13,.2f} {currency}"


def _accumulated_savings(monthly_contribution: float, months: float, monthly_rate: float) -> float:
    if monthly_rate == 0:
        return monthly_contribution * months
    return monthly_contribution * ((1 + monthly_rate) ** months - 1) / monthly_rate


def _required_nest_egg(monthly_payout: float, months: float, monthly_rate: float) -> float:
    if monthly_rate == 0:
        return monthly_payout * months
    return monthly_payout * (1 - (1 + monthly_rate) ** -months) / monthly_rate


def solve_monthly_contribution(interest_rate: float, accumulation_years: float,
                               monthly_payout: float, payout_years: float) -> tuple[float, float]:
    m = interest_rate / 12
    n = accumulation_years * 12
    k = payout_years * 12
    fv = _required_nest_egg(monthly_payout, k, m)
    if m == 0:
        contribution = fv / n
    else:
        contribution = fv * m / ((1 + m) ** n - 1)
    return contribution, fv


def solve_accumulation_years(interest_rate: float, monthly_contribution: float,
                             monthly_payout: float, payout_years: float) -> tuple[float, float]:
    m = interest_rate / 12
    k = payout_years * 12
    fv = _required_nest_egg(monthly_payout, k, m)
    if m == 0:
        years = fv / monthly_contribution / 12
    else:
        years = math.log(fv * m / monthly_contribution + 1) / math.log(1 + m) / 12
    return years, fv


def solve_monthly_payout(interest_rate: float, monthly_contribution: float,
                         accumulation_years: float, payout_years: float) -> tuple[float, float]:
    m = interest_rate / 12
    n = accumulation_years * 12
    k = payout_years * 12
    fv = _accumulated_savings(monthly_contribution, n, m)
    if m == 0:
        payout = fv / k
    else:
        payout = fv * m / (1 - (1 + m) ** -k)
    return payout, fv


def solve_payout_years(interest_rate: float, monthly_contribution: float,
                       accumulation_years: float, monthly_payout: float) -> tuple[float, float]:
    m = interest_rate / 12
    n = accumulation_years * 12
    fv = _accumulated_savings(monthly_contribution, n, m)
    if m == 0:
        years = fv / monthly_payout / 12
    else:
        ratio = fv * m / monthly_payout
        if ratio >= 1:
            years = float("inf")
        else:
            years = -math.log(1 - ratio) / math.log(1 + m) / 12
    return years, fv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--currency", default="€")
    args = parser.parse_args()
    c = args.currency

    print("=== Retirement Calculator ===\n")
    print("Solve for:")
    print("  1. Monthly contribution")
    print("  2. Accumulation years")
    print("  3. Monthly payout")
    print("  4. Payout years")

    choice = input("\nYour choice (1-4): ").strip()
    interest_rate = float(input("Annual interest rate (%): ")) / 100

    if choice == "1":
        accumulation_years = float(input("Accumulation years: "))
        monthly_payout = float(input(f"Monthly payout ({c}): "))
        payout_years = float(input("Payout years: "))
        result, fv = solve_monthly_contribution(interest_rate, accumulation_years, monthly_payout, payout_years)
        print(f"\nAccumulated savings:   {_fmt(fv, c)}")
        print(f"Monthly contribution:  {_fmt(result, c)}")

    elif choice == "2":
        monthly_contribution = float(input(f"Monthly contribution ({c}): "))
        monthly_payout = float(input(f"Monthly payout ({c}): "))
        payout_years = float(input("Payout years: "))
        result, fv = solve_accumulation_years(interest_rate, monthly_contribution, monthly_payout, payout_years)
        print(f"\nAccumulated savings:   {_fmt(fv, c)}")
        print(f"Accumulation years:    {result:>14.2f}")

    elif choice == "3":
        monthly_contribution = float(input(f"Monthly contribution ({c}): "))
        accumulation_years = float(input("Accumulation years: "))
        payout_years = float(input("Payout years: "))
        result, fv = solve_monthly_payout(interest_rate, monthly_contribution, accumulation_years, payout_years)
        print(f"\nAccumulated savings:   {_fmt(fv, c)}")
        print(f"Monthly payout:        {_fmt(result, c)}")

    elif choice == "4":
        monthly_contribution = float(input(f"Monthly contribution ({c}): "))
        accumulation_years = float(input("Accumulation years: "))
        monthly_payout = float(input(f"Monthly payout ({c}): "))
        result, fv = solve_payout_years(interest_rate, monthly_contribution, accumulation_years, monthly_payout)
        print(f"\nAccumulated savings:   {_fmt(fv, c)}")
        if result == float("inf"):
            print(f"Payout years:          indefinitely (interest covers payout)")
        else:
            print(f"Payout years:          {result:>14.2f}")

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
