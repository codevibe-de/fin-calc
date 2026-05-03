def calculate_monthly_payment(principal: float, annual_rate: float, months: int) -> float:
    if annual_rate == 0:
        return principal / months
    monthly_rate = annual_rate / 100 / 12
    return principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)


def main():
    print("=== Loan Calculator ===\n")

    principal = float(input("Loan amount: "))
    annual_rate = float(input("Annual interest rate (%): "))
    years = float(input("Duration (years): "))

    months = int(years * 12)
    monthly = calculate_monthly_payment(principal, annual_rate, months)
    total = monthly * months
    total_interest = total - principal

    print(f"\nMonthly payment:  {monthly:>10.2f}")
    print(f"Total repaid:     {total:>10.2f}")
    print(f"Total interest:   {total_interest:>10.2f}")


if __name__ == "__main__":
    main()
