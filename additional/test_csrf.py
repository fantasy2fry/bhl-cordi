from flask import Flask, request

app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def submit():
    # Assume data processing without CSRF protection
    data = request.form['data']
    print("Data received:", data)
    return "Data processed"


if __name__ == "__main__":
    app.run(debug=True)
