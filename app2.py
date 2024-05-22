from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Witaj, to jest strona główna!"

@app.route('/exchange', methods=['GET', 'POST'])
def exchange():
    if request.method == 'GET':
        return render_template('exchange.html')
    else:
        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']

        amount = 100
        if 'amount' in request.form:
            amount = request.form['amount']

        return render_template('exchange_result.html', currency=currency, amount=amount)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
