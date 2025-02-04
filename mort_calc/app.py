from flask import Flask, request, render_template, send_file
from decimal import Decimal, getcontext, InvalidOperation
import csv
from io import StringIO, BytesIO
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any

# Set decimal precision for financial calculations
getcontext().prec = 12

app = Flask(__name__)

@dataclass
class LoanParams:
    """Data class to store loan parameters."""
    loan_amount: Decimal
    loan_term: int
    interest_rate: Decimal
    remaining_term: int
    extra_payment_monthly: Decimal = Decimal('0')
    extra_payment_annual: Decimal = Decimal('0')
    extra_payment_onetime: Decimal = Decimal('0')

def validate_inputs(params: LoanParams) -> None:
    """Validate all input parameters."""
    if params.loan_amount <= 0:
        raise ValueError("Loan amount must be greater than 0")
    if params.loan_term <= 0 or params.loan_term > 40:
        raise ValueError("Loan term must be between 1 and 40 years")
    if params.interest_rate <= 0 or params.interest_rate > Decimal('30'):
        raise ValueError("Interest rate must be between 0 and 30%")
    if params.remaining_term <= 0 or params.remaining_term > params.loan_term:
        raise ValueError("Remaining term must be between 1 and the loan term")

def has_extra_payments(params: LoanParams) -> bool:
    """Check if any extra payments are provided."""
    return (params.extra_payment_monthly > 0 or
            params.extra_payment_annual > 0 or
            params.extra_payment_onetime > 0)

def calculate_monthly_payment(loan_amount: Decimal, interest_rate: Decimal, term: int) -> Decimal:
    """Calculate regular monthly payment amount."""
    if term == 0:
        return loan_amount
    monthly_rate = interest_rate / 12
    n_payments = term * 12
    return loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)

def calculate_loan_balance_at_period(loan_amount: Decimal, interest_rate: Decimal,
                                   monthly_payment: Decimal, periods: int) -> Decimal:
    """Calculate loan balance after a given number of periods."""
    monthly_rate = interest_rate / 12
    balance = loan_amount

    for _ in range(periods):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment

    return balance

def get_payoff_time(table: List[Dict]) -> Tuple[int, int]:
    """Calculate the payoff time in years and months from an amortization table."""
    total_months = len(table)
    years = total_months // 12
    months = total_months % 12
    return years, months

def calculate_amortization(params: LoanParams) -> Tuple[List[Dict], Decimal, List[Dict], Decimal]:
    """
    Calculate amortization schedules for both normal and extra payment scenarios.
    Returns: (extra_payment_table, extra_payment_interest, normal_table, normal_interest)
    """
    monthly_rate = params.interest_rate / 12

    # Calculate normal payment schedule
    normal_balance = params.loan_amount
    normal_payment = calculate_monthly_payment(params.loan_amount, params.interest_rate, params.remaining_term)
    normal_total_interest = Decimal('0')
    normal_table = []

    for month in range(1, params.remaining_term * 12 + 1):
        interest_payment = normal_balance * monthly_rate
        principal_payment = normal_payment - interest_payment
        normal_balance = max(Decimal('0'), normal_balance - principal_payment)
        normal_total_interest += interest_payment

        normal_table.append({
            "Month": month,
            "Payment": round(normal_payment, 2),
            "Interest": round(interest_payment, 2),
            "Principal": round(principal_payment, 2),
            "Balance": round(normal_balance, 2)
        })

    # If no extra payments, return normal schedule twice
    if not has_extra_payments(params):
        return normal_table, normal_total_interest, normal_table, normal_total_interest

    # Calculate schedule with extra payments
    extra_balance = params.loan_amount
    base_payment = normal_payment
    extra_total_interest = Decimal('0')
    extra_table = []

    for month in range(1, params.remaining_term * 12 + 1):
        payment = base_payment

        # Add extra payments
        payment += params.extra_payment_monthly
        if month % 12 == 0:
            payment += params.extra_payment_annual
        if month == 1:
            payment += params.extra_payment_onetime

        interest_payment = extra_balance * monthly_rate
        principal_payment = payment - interest_payment

        if extra_balance < payment:
            principal_payment = extra_balance
            payment = extra_balance + interest_payment

        extra_balance = max(Decimal('0'), extra_balance - principal_payment)
        extra_total_interest += interest_payment

        extra_table.append({
            "Month": month,
            "Payment": round(payment, 2),
            "Interest": round(interest_payment, 2),
            "Principal": round(principal_payment, 2),
            "Balance": round(extra_balance, 2)
        })

        if extra_balance == 0:
            break

    return extra_table, extra_total_interest, normal_table, normal_total_interest

def create_loan_params_from_request(request_form: Dict) -> LoanParams:
    """Create LoanParams object from form data."""
    return LoanParams(
        loan_amount=Decimal(str(request_form["loan_amount"])),
        loan_term=int(request_form["loan_term"]),
        interest_rate=Decimal(str(request_form["interest_rate"])) / 100,
        remaining_term=int(request_form["remaining_term"]),
        extra_payment_monthly=Decimal(str(request_form.get("extra_payment_monthly", "0"))),
        extra_payment_annual=Decimal(str(request_form.get("extra_payment_annual", "0"))),
        extra_payment_onetime=Decimal(str(request_form.get("extra_payment_onetime", "0")))
    )

def adjust_loan_for_remaining_term(params: LoanParams) -> None:
    """Adjust loan amount based on payments already made if remaining term < loan term."""
    if params.remaining_term < params.loan_term:
        periods_passed = (params.loan_term - params.remaining_term) * 12
        monthly_payment = calculate_monthly_payment(params.loan_amount, params.interest_rate, params.loan_term)
        params.loan_amount = calculate_loan_balance_at_period(
            params.loan_amount, params.interest_rate, monthly_payment, periods_passed
        )

def generate_csv_content(table: List[Dict]) -> str:
    """Generate CSV content from amortization table."""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Month", "Payment", "Interest", "Principal", "Balance"])
    for row in table:
        writer.writerow([
            row["Month"],
            f"{row['Payment']:.2f}",
            f"{row['Interest']:.2f}",
            f"{row['Principal']:.2f}",
            f"{row['Balance']:.2f}"
        ])
    return output.getvalue()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Store form data for persistence
            form_data = {
                "loan_amount": request.form["loan_amount"],
                "loan_term": request.form["loan_term"],
                "interest_rate": request.form["interest_rate"],
                "remaining_term": request.form["remaining_term"],
                "extra_payment_monthly": request.form.get("extra_payment_monthly", "0"),
                "extra_payment_annual": request.form.get("extra_payment_annual", "0"),
                "extra_payment_onetime": request.form.get("extra_payment_onetime", "0")
            }

            try:
                # Process loan parameters
                params = create_loan_params_from_request(form_data)
                validate_inputs(params)
                adjust_loan_for_remaining_term(params)

                # Calculate amortization schedules
                extra_table, extra_interest, normal_table, normal_interest = calculate_amortization(params)

                # Calculate payoff times
                extra_years, extra_months = get_payoff_time(extra_table)
                normal_years, normal_months = params.remaining_term, 0

                return render_template(
                    "index.html",
                    table=extra_table,
                    total_interest=extra_interest,
                    normal_total_interest=normal_interest,
                    form_data=form_data,
                    has_extra_payments=has_extra_payments(params),
                    comparison={
                        "extra_years": extra_years,
                        "extra_months": extra_months,
                        "normal_years": normal_years,
                        "normal_months": normal_months,
                        "interest_saved": normal_interest - extra_interest
                    }
                )

            except (ValueError, InvalidOperation) as e:
                return render_template("index.html", error=f"Invalid input: {str(e)}", form_data=form_data)

        except Exception as e:
            return render_template("index.html", error=f"An unexpected error occurred: {str(e)}", form_data=form_data)

    return render_template("index.html", form_data={})

@app.route("/download", methods=["POST"])
def download_csv():
    try:
        params = create_loan_params_from_request(request.form)
        validate_inputs(params)
        adjust_loan_for_remaining_term(params)

        table, _, _, _ = calculate_amortization(params)

        # Generate and send CSV file
        output = BytesIO()
        output.write(generate_csv_content(table).encode('utf-8'))
        output.seek(0)

        return send_file(
            output,
            mimetype="text/csv",
            as_attachment=True,
            download_name="amortization_schedule.csv"
        )
    except (ValueError, InvalidOperation) as e:
        return str(e), 400
    except Exception as e:
        return f"An error occurred while generating the CSV file: {str(e)}", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9099, debug=True)
