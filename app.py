from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>YAYYY</h1>'

@app.route('/about')
def about():
    return '<h1>EEEEE</h1>'

if __name__ == '__main__':
    app.run(debug=True)  # Domyślnie używa portu 5000
