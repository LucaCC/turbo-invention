from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__)


@app.route("/")
def intro():
    with open('primary elections 2016.json') as election_data:
        electionData = json.load(election_data)
    return render_template('Political_Demographic_Intro.html')


if __name__ == "__main__":
    app.run(debug=False)
