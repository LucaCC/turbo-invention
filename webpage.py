from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__)


@app.route("/")
def intro():
    return render_template('Political_Demographic_Intro.html')

@app.route("/StateCounty")
def First_Page():
    with open('Primary_Elections_2016.json') as election_data:
        electionData = json.load(election_data)
    return render_template('Political_Demographic_Dropdown.html', candidate=get_candidate_options(electionData), c_info=political_party(request.args['candidate'], electionData), c=request.args['candidate'])

def get_candidate_options(election_data):
    candidate = []
    for data in election_data:
        for a in data["Vote Data"].keys():
            if a not in candidate:
                candidate.append(a)
    options = ""
    for data in candidate:
        options = options + \
            Markup("<option value=\"" + data + "\">" + data + "</option>")

def political_party(candidate_chosen, election_data):
    political_party = ""
    key = "Political Party: "
    for data in election_data:
        if data["Vote Data"] == candidate_chosen:
            political_party = data["Vote Data"]["Party"]

    return key + str(political_party)

    return options

if __name__ == "__main__":
    app.run(debug=False)
