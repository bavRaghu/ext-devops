from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("registration.html")

@app.route("/register", methods=['POST'])
def register():
    n = request.form['n']
    pw = request.form['pw']
    return render_template('success.html', n=n, pw=pw)

if __name__ == '__main__':
    app.run(port=5003, debug=False)