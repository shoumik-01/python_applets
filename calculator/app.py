from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')
    operation = data.get('operation')

    def format_number(num):
        if isinstance(num, float):
            num = round(num, 10)  # Round to 10 decimal places
        return int(num) if num.is_integer() else num

    try:
        num1 = float(num1)
        num2 = float(num2) if num2 else None

        # Original operations
        if operation == 'add':
            result = num1 + num2
            operationPerformed = f'{format_number(num1)} + {format_number(num2)} = {format_number(result)}'
        elif operation == 'subtract':
            result = num1 - num2
            operationPerformed = f'{format_number(num1)} - {format_number(num2)} = {format_number(result)}'
        elif operation == 'multiply':
            result = num1 * num2
            operationPerformed = f'{format_number(num1)} * {format_number(num2)} = {format_number(result)}'
        elif operation == 'divide':
            if num2 == 0:
                return jsonify(error='Division by zero leads to the singularity...'), 400
            result = num1 / num2
            operationPerformed = f'{format_number(num1)} / {format_number(num2)} = {format_number(result)}'
        elif operation == 'square':
            result = num1 ** 2
            operationPerformed = f'{format_number(num1)}^2 = {format_number(result)}'
        elif operation == 'sqrt':
            if num1 < 0:
                return jsonify(error='Cannot calculate square root of a negative number'), 400
            result = math.sqrt(num1)
            operationPerformed = f'√({format_number(num1)}) = {format_number(result)}'
        elif operation == 'binary':
            if num1 < 0 or not num1.is_integer():
                return jsonify(error='Binary conversion requires a positive integer'), 400
            result = bin(int(num1))[2:]
            operationPerformed = f'bin({int(num1)}) = {result}'
        elif operation == 'sin':
            result = math.sin(math.radians(num1))
            operationPerformed = f'sin({format_number(num1)}°) = {format_number(result)}'
        elif operation == 'cos':
            result = math.cos(math.radians(num1))
            operationPerformed = f'cos({format_number(num1)}°) = {format_number(result)}'
        elif operation == 'tan':
            if abs(math.cos(math.radians(num1))) < 1e-10:
                return jsonify(error='Tangent undefined at 90° or 270°'), 400
            result = math.tan(math.radians(num1))
            operationPerformed = f'tan({format_number(num1)}°) = {format_number(result)}'

        # New operations
        elif operation == 'power':
            result = num1 ** num2
            operationPerformed = f'{format_number(num1)}^{format_number(num2)} = {format_number(result)}'
        elif operation == 'log':
            if num1 <= 0:
                return jsonify(error='Cannot calculate logarithm of non-positive number'), 400
            result = math.log10(num1)
            operationPerformed = f'log₁₀({format_number(num1)}) = {format_number(result)}'
        elif operation == 'ln':
            if num1 <= 0:
                return jsonify(error='Cannot calculate natural logarithm of non-positive number'), 400
            result = math.log(num1)
            operationPerformed = f'ln({format_number(num1)}) = {format_number(result)}'
        elif operation == 'factorial':
            if num1 < 0 or not num1.is_integer():
                return jsonify(error='Factorial requires a non-negative integer'), 400
            if num1 > 170:  # Prevent overflow
                return jsonify(error='Number too large for factorial calculation'), 400
            result = math.factorial(int(num1))
            operationPerformed = f'{int(num1)}! = {result}'
        elif operation == 'abs':
            result = abs(num1)
            operationPerformed = f'|{format_number(num1)}| = {format_number(result)}'
        elif operation == 'hex':
            if num1 < 0 or not num1.is_integer():
                return jsonify(error='Hexadecimal conversion requires a positive integer'), 400
            result = hex(int(num1))[2:].upper()  # Remove '0x' prefix and capitalize
            operationPerformed = f'hex({int(num1)}) = {result}'
        else:
            return jsonify(error='Invalid operation'), 400

        return jsonify(result=result, operationPerformed=operationPerformed)
    except ValueError:
        return jsonify(error='Invalid input'), 400

if __name__ == '__main__':
    app.run()
