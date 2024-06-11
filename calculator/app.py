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
            result = math.sqrt(num1)
            operationPerformed = f'√({format_number(num1)}) = {format_number(result)}'
        elif operation == 'binary':
            result = bin(int(num1))[2:]  # Convert to binary and remove '0b' prefix
            operationPerformed = f'bin({int(num1)}) = {result}'
        elif operation == 'sin':
            result = math.sin(math.radians(num1))  # Convert degrees to radians
            operationPerformed = f'sin({format_number(num1)}°) = {result}'
        elif operation == 'cos':
            result = math.cos(math.radians(num1))  # Convert degrees to radians
            operationPerformed = f'cos({format_number(num1)}°) = {result}'
        elif operation == 'tan':
            result = math.tan(math.radians(num1))  # Convert degrees to radians
            operationPerformed = f'tan({format_number(num1)}°) = {result}'
        else:
            return jsonify(error='Invalid operation'), 400

        return jsonify(result=result, operationPerformed=operationPerformed)
    except ValueError:
        return jsonify(error='Invalid input'), 400

if __name__ == '__main__':
    app.run()
