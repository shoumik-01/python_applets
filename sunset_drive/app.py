from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    # Extract parameters from request
    current_age = int(data.get('currentAge'))
    retirement_age = int(data.get('retirementAge'))
    life_expectancy = int(data.get('lifeExpectancy', 90))  # Default life expectancy
    current_income = float(data.get('currentIncome'))
    income_growth_rate = float(data.get('incomeGrowthRate')) / 100  # Convert percentage to decimal
    current_savings = float(data.get('currentSavings'))
    savings_rate = float(data.get('savingsRate')) / 100  # Convert percentage to decimal
    investment_return = float(data.get('investmentReturn', 7)) / 100  # Default 7%, convert to decimal
    retirement_spending = float(data.get('retirementSpending'))

    # Social Security parameters
    ss_benefit_monthly = float(data.get('ssBenefit', 0))
    ss_benefit_annual = ss_benefit_monthly * 12  # Convert monthly to annual
    ss_start_age = int(data.get('ssStartAge', 67))  # Default to full retirement age of 67

    # Calculate retirement savings growth over time
    result = calculate_retirement_projection(
        current_age, retirement_age, life_expectancy,
        current_income, income_growth_rate,
        current_savings, savings_rate, investment_return,
        retirement_spending, ss_benefit_annual, ss_start_age
    )

    return jsonify(result)


@app.route('/compare', methods=['POST'])
def compare():
    data = request.json
    scenario1 = data.get('scenario1', {})
    scenario2 = data.get('scenario2', {})

    # Process each scenario
    result1 = calculate_retirement_projection(
        int(scenario1.get('currentAge')),
        int(scenario1.get('retirementAge')),
        int(scenario1.get('lifeExpectancy')),
        float(scenario1.get('currentIncome')),
        float(scenario1.get('incomeGrowthRate')) / 100,
        float(scenario1.get('currentSavings')),
        float(scenario1.get('savingsRate')) / 100,
        float(scenario1.get('investmentReturn')) / 100,
        float(scenario1.get('retirementSpending')),
        float(scenario1.get('ssBenefit', 0)) * 12,
        int(scenario1.get('ssStartAge', 67))
    )

    result2 = calculate_retirement_projection(
        int(scenario2.get('currentAge')),
        int(scenario2.get('retirementAge')),
        int(scenario2.get('lifeExpectancy')),
        float(scenario2.get('currentIncome')),
        float(scenario2.get('incomeGrowthRate')) / 100,
        float(scenario2.get('currentSavings')),
        float(scenario2.get('savingsRate')) / 100,
        float(scenario2.get('investmentReturn')) / 100,
        float(scenario2.get('retirementSpending')),
        float(scenario2.get('ssBenefit', 0)) * 12,
        int(scenario2.get('ssStartAge', 67))
    )

    # Build comparison data
    comparison_data = {
        'scenario1': result1,
        'scenario2': result2
    }

    return jsonify(comparison_data)


def calculate_retirement_projection(
    current_age, retirement_age, life_expectancy,
    current_income, income_growth_rate,
    current_savings, savings_rate, investment_return,
    retirement_spending, ss_benefit_annual, ss_start_age
):
    # Calculate retirement savings growth over time
    years = list(range(current_age, life_expectancy + 1))
    savings = [current_savings]
    income = current_income

    for age in range(current_age + 1, life_expectancy + 1):
        last_savings = savings[-1]

        # Apply investment returns to existing savings
        investment_growth = last_savings * investment_return

        # Initialize annual income from Social Security
        ss_income = 0

        if age >= ss_start_age:
            ss_income = ss_benefit_annual

        if age <= retirement_age:
            # Working years - add savings
            income = income * (1 + income_growth_rate)  # Income grows each year
            annual_contribution = income * savings_rate
            new_savings = last_savings + annual_contribution + investment_growth
        else:
            # Retirement years - withdraw funds
            withdrawal = retirement_spending - ss_income  # Reduce withdrawals by SS income
            withdrawal = max(0, withdrawal)  # Ensure withdrawal is not negative
            new_savings = last_savings + investment_growth - withdrawal

        # Ensure savings don't go below zero
        new_savings = max(0, new_savings)
        savings.append(new_savings)

    # Prepare data for the chart
    chart_data = {
        'labels': years,
        'datasets': [
            {
                'label': 'Retirement Savings',
                'data': savings,
                'borderColor': '#39FF14',  # Neon green
                'backgroundColor': 'rgba(57, 255, 20, 0.1)'
            }
        ]
    }

    # Additional analytics
    max_savings = max(savings)
    max_savings_age = years[savings.index(max_savings)]
    retirement_fund_depletion_age = None

    for i, amount in enumerate(savings):
        if amount <= 0 and i > 0 and savings[i-1] > 0:
            retirement_fund_depletion_age = years[i]
            break

    analytics = {
        'maxSavings': round(max_savings, 2),
        'maxSavingsAge': max_savings_age,
        'retirementFundDepletionAge': retirement_fund_depletion_age,
        'ssIncome': round(ss_benefit_annual, 2)
    }

    return {
        'chartData': chart_data,
        'analytics': analytics
    }


if __name__ == '__main__':
    app.run(debug=True)
