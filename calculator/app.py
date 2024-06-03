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

    try:
        num1 = float(num1)
        num2 = float(num2) if num2 else None

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return jsonify(error='Division by zero is not allowed'), 400
            result = num1 / num2
        elif operation == 'square':
            result = num1 ** 2
        elif operation == 'sqrt':
            result = math.sqrt(num1)
        elif operation == 'binary':
            result = bin(int(num1))[2:]  # Convert to binary and remove '0b' prefix
        elif operation == 'sin':
            result = math.sin(math.radians(num1))  # Convert degrees to radians
        elif operation == 'cos':
            result = math.cos(math.radians(num1))  # Convert degrees to radians
        elif operation == 'tan':
            result = math.tan(math.radians(num1))  # Convert degrees to radians
        else:
            return jsonify(error='Invalid operation'), 400

        return jsonify(result=result)
    except ValueError:
        return jsonify(error='Invalid input'), 400

if __name__ == '__main__':
    app.run()
