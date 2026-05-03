def calculate_monthly_payment(p: float, r: float, n: int) -> None:
    if r == 0:
        x = p / n
    else:
        m = r / 100 / 12
        x = p * m / (1 - (1 + m) ** -n)

    print(f"\nMonthly payment:  {x:>10.2f}")
    print(f"Total repaid:     {x * n:>10.2f}")
    print(f"Total interest:   {x * n - p:>10.2f}")


def main():
    print("=== Loan Calculator ===\n")

    p = float(input("Loan amount: "))
    r = float(input("Annual interest rate (%): "))
    y = float(input("Duration (years): "))

    n = int(y * 12)
    calculate_monthly_payment(p, r, n)


if __name__ == "__main__":
    main()