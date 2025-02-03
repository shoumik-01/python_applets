from flask import Flask, request, render_template, send_file
from decimal import Decimal, getcontext, InvalidOperation
import csv
from io import StringIO, BytesIO

# Set decimal precision for financial calculations
getcontext().prec = 12

app = Flask(__name__)

def validate_inputs(loan_amount, loan_term, interest_rate, remaining_term):
    """Validate input parameters."""
    if loan_amount <= 0:
        raise ValueError("Loan amount must be greater than 0")
    if loan_term <= 0 or loan_term > 40:
        raise ValueError("Loan term must be between 1 and 40 years")
    if interest_rate <= 0 or interest_rate > 30:
        raise ValueError("Interest rate must be between 0 and 30%")
    if remaining_term <= 0 or remaining_term > loan_term:
        raise ValueError("Remaining term must be between 1 and the loan term")

def calculate_payment(loan_amount, interest_rate, term):
    """Calculate monthly payment."""
    if term == 0:
        return loan_amount
    monthly_rate = interest_rate / 12
    n_payments = term * 12
    return loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)

def calculate_amortization(loan_amount, term, interest_rate, repayment_option, extra_payment):
    """Calculate the amortization schedule with various repayment options."""
    monthly_rate = interest_rate / 12
    balance = loan_amount
    total_interest = Decimal('0')
    table = []

    if repayment_option == "biweekly":
        # Biweekly calculations
        # Calculate proper biweekly payment (26 payments per year)
        yearly_payment = calculate_payment(loan_amount, interest_rate, term) * 12
        biweekly_payment = yearly_payment / 26
        n_payments = term * 26

        monthly_interest = Decimal('0')
        monthly_principal = Decimal('0')

        # Convert to Decimal for the power calculation
        one = Decimal('1')
        two = Decimal('2')

        for payment_num in range(1, n_payments + 1):
            # Calculate effective biweekly rate using Decimal math
            effective_biweekly_rate = (one + monthly_rate) ** (one/two) - one
            interest_payment = balance * effective_biweekly_rate
            principal_payment = biweekly_payment - interest_payment

            # Adjust final payment if needed
            if balance < biweekly_payment:
                principal_payment = balance
                biweekly_payment = balance + interest_payment

            balance = max(Decimal('0'), balance - principal_payment)

            # Accumulate biweekly amounts
            monthly_interest += interest_payment
            monthly_principal += principal_payment

            # Record in table every two payments (monthly)
            if payment_num % 2 == 0:
                month = payment_num // 2
                table.append({
                    "Month": month,
                    "Payment": round(biweekly_payment * 2, 2),
                    "Interest": round(monthly_interest, 2),
                    "Principal": round(monthly_principal, 2),
                    "Balance": round(balance, 2)
                })
                total_interest += monthly_interest
                monthly_interest = Decimal('0')
                monthly_principal = Decimal('0')

            if balance == 0:
                break

    elif repayment_option == "normal":
        # Regular monthly payment calculations
        monthly_payment = calculate_payment(loan_amount, interest_rate, term)
        n_payments = term * 12

        for month in range(1, n_payments + 1):
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment

            # Adjust final payment if needed
            if balance < monthly_payment:
                principal_payment = balance
                monthly_payment = balance + interest_payment

            balance = max(Decimal('0'), balance - principal_payment)
            total_interest += interest_payment

            table.append({
                "Month": month,
                "Payment": round(monthly_payment, 2),
                "Interest": round(interest_payment, 2),
                "Principal": round(principal_payment, 2),
                "Balance": round(balance, 2)
            })

            if balance == 0:
                break

    else:
        # Extra payment calculations (monthly or annual)
        monthly_payment = calculate_payment(loan_amount, interest_rate, term)
        n_payments = term * 12

        for month in range(1, n_payments + 1):
            payment = monthly_payment

            # Add extra payments
            if repayment_option == "extra_monthly":
                payment += extra_payment
            elif repayment_option == "extra_annual" and month % 12 == 0:
                payment += extra_payment

            interest_payment = balance * monthly_rate
            principal_payment = payment - interest_payment

            if balance < payment:
                principal_payment = balance
                payment = balance + interest_payment

            balance = max(Decimal('0'), balance - principal_payment)
            total_interest += interest_payment

            table.append({
                "Month": month,
                "Payment": round(payment, 2),
                "Interest": round(interest_payment, 2),
                "Principal": round(principal_payment, 2),
                "Balance": round(balance, 2)
            })

            if balance == 0:
                break

    return table, total_interest

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
                "repayment_option": request.form["repayment_option"],
                "extra_payment": request.form.get("extra_payment", "0")
            }

            try:
                # Convert form data for calculations
                loan_amount = Decimal(str(form_data["loan_amount"]))
                loan_term = int(form_data["loan_term"])
                interest_rate = Decimal(str(form_data["interest_rate"])) / 100
                remaining_term = int(form_data["remaining_term"])
                repayment_option = form_data["repayment_option"]
                extra_payment = Decimal(str(form_data["extra_payment"]))

                # Validate inputs
                validate_inputs(loan_amount, loan_term, interest_rate, remaining_term)

                # Calculate initial amortization to get to the starting point of remaining term
                if remaining_term < loan_term:
                    periods_passed = (loan_term - remaining_term) * 12
                    monthly_rate = interest_rate / 12
                    monthly_payment = calculate_payment(loan_amount, interest_rate, loan_term)

                    balance = loan_amount
                    for _ in range(periods_passed):
                        interest_payment = balance * monthly_rate
                        principal_payment = monthly_payment - interest_payment
                        balance -= principal_payment
                    loan_amount = balance

                # Calculate amortization schedule
                table, total_interest = calculate_amortization(
                    loan_amount, remaining_term, interest_rate,
                    repayment_option, extra_payment
                )

                return render_template(
                    "index.html",
                    table=table,
                    total_interest=total_interest,
                    form_data=form_data
                )

            except (ValueError, InvalidOperation) as e:
                return render_template("index.html", error=f"Invalid input: {str(e)}", form_data=form_data)

        except Exception as e:
            return render_template("index.html", error=f"An unexpected error occurred: {str(e)}", form_data=form_data)

    return render_template("index.html", form_data={})

@app.route("/download", methods=["POST"])
def download_csv():
    try:
        # Collect the table data with proper error handling
        loan_amount = Decimal(str(request.form.get("loan_amount", "0")))
        loan_term = int(request.form.get("loan_term", "0"))
        interest_rate = Decimal(str(request.form.get("interest_rate", "0"))) / 100
        remaining_term = int(request.form.get("remaining_term", "0"))
        repayment_option = request.form.get("repayment_option", "normal")
        extra_payment = Decimal(str(request.form.get("extra_payment", "0")))

        # Validate inputs
        validate_inputs(loan_amount, loan_term, interest_rate, remaining_term)

        # Calculate initial amortization to get to the starting point of remaining term
        if remaining_term < loan_term:
            periods_passed = (loan_term - remaining_term) * 12
            monthly_rate = interest_rate / 12
            monthly_payment = calculate_payment(loan_amount, interest_rate, loan_term)

            balance = loan_amount
            for _ in range(periods_passed):
                interest_payment = balance * monthly_rate
                principal_payment = monthly_payment - interest_payment
                balance -= principal_payment
            loan_amount = balance

        # Calculate amortization schedule
        table, _ = calculate_amortization(
            loan_amount, remaining_term, interest_rate,
            repayment_option, extra_payment
        )

        # Generate CSV file using BytesIO
        output = BytesIO()
        output_str = StringIO()
        writer = csv.writer(output_str)
        writer.writerow(["Month", "Payment", "Interest", "Principal", "Balance"])
        for row in table:
            writer.writerow([
                row["Month"],
                f"{row['Payment']:.2f}",
                f"{row['Interest']:.2f}",
                f"{row['Principal']:.2f}",
                f"{row['Balance']:.2f}"
            ])

        output.write(output_str.getvalue().encode('utf-8'))
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
