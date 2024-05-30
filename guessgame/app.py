from flask import Flask, render_template, request, session, jsonify
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    session['number'] = random.randint(1, 20)
    session['attempts'] = 0
    session['guesses'] = []
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    guess = int(request.form['guess'])
    correct_number = session.get('number')
    session['attempts'] += 1
    session['guesses'].append(guess)

    if guess < correct_number:
        message = 'Your guess is too low'
    elif guess > correct_number:
        message = 'Your guess is too high'
    else:
        message = 'You won!! The correct number was ' + str(correct_number)
        return jsonify(message=message, game_over=True, guesses=session['guesses'])

    if session['attempts'] >= 3:
        message = 'Better luck next time! The correct number was ' + str(correct_number)
        return jsonify(message=message, game_over=True, guesses=session['guesses'])

    return jsonify(message=message, game_over=False, guesses=session['guesses'])

@app.route('/restart', methods=['POST'])
def restart():
    session['number'] = random.randint(1, 20)
    session['attempts'] = 0
    session['guesses'] = []
    return jsonify(message='Game restarted', game_over=False, guesses=[])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9092)
