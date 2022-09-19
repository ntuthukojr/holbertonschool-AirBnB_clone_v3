#!/usr/bin/python3
"""task 6"""

from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """say hello"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """hi holberton"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """C"""
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    """python"""
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def num(n):
    """n"""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def nt(n):
    """number template"""
    return render_template("5-number.html", var=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def noe(n):
    """number template"""
    if (n % 2) == 0:
        return render_template("6-number_odd_or_even.html",
                               var="{} is even".format(n))
    return render_template("6-number_odd_or_even.html",
                           var="{} is odd".format(n))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
