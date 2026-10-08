import argparse
from typing import NamedTuple


class Row(NamedTuple):
    period: int
    interest: float
    principal: float
    balance: float


def monthly_payment(principal: float, annual_rate_pct: float, months: int) -> float:
    # annuity payment for a loan repaid in equal monthly instalments
    if annual_rate_pct == 0:
        return principal / months
    m = annual_rate_pct / 100 / 12
    return principal * m / (1 - (1 + m) ** -months)


def amortization_schedule(principal: float, annual_rate_pct: float, months: int) -> list[Row]:
    # one row per monthly instalment: interest, principal repaid and remaining balance
    m = annual_rate_pct / 100 / 12
    payment = monthly_payment(principal, annual_rate_pct, months)
    balance = principal
    rows = []
    for month in range(1, months + 1):
        interest = balance * m
        repaid = payment - interest
        if month == months:
            repaid = balance
        balance -= repaid
        if month == months:
            balance = 0.0
        rows.append(Row(month, interest, repaid, balance))
    return rows


def yearly(rows: list[Row]) -> list[Row]:
    # condenses monthly rows into one row per year; a partial last year keeps only its months
    years = []
    for start in range(0, len(rows), 12):
        chunk = rows[start:start + 12]
        years.append(Row(start // 12 + 1,
                         sum(r.interest for r in chunk),
                         sum(r.principal for r in chunk),
                         chunk[-1].balance))
    return years


def print_schedule(rows: list[Row], label: str) -> None:
    # prints the schedule as an aligned table
    print(f"\n{label:>5}  {'Interest':>12}  {'Principal':>12}  {'Balance':>12}")
    for r in rows:
        print(f"{r.period:>5}  {r.interest:>12.2f}  {r.principal:>12.2f}  {r.balance:>12.2f}")


def calculate_monthly_payment(p: float, r: float, n: int) -> None:
    # computes and prints monthly payment, total repaid, and total interest
    x = monthly_payment(p, r, n)

    print(f"\nMonthly payment:  {x:>10.2f}")
    print(f"Total repaid:     {x * n:>10.2f}")
    print(f"Total interest:   {x * n - p:>10.2f}")


def main():
    # entry point: prompts for loan details and prints the repayment breakdown and schedule
    parser = argparse.ArgumentParser()
    parser.add_argument("--monthly", action="store_true", help="show the schedule month by month")
    args = parser.parse_args()

    print("=== Loan Calculator ===\n")

    p = float(input("Loan amount: "))
    r = float(input("Annual interest rate (%): "))
    y = float(input("Duration (years): "))

    n = int(y * 12)
    calculate_monthly_payment(p, r, n)

    rows = amortization_schedule(p, r, n)
    if args.monthly:
        print_schedule(rows, "Month")
    else:
        print_schedule(yearly(rows), "Year")


if __name__ == "__main__":
    main()
