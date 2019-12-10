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
        if 'candidate' in request.args:
            return render_template('Political_Demographic_Dropdown.html', candidate=get_candidate_options(electionData),
            c_info=political_party(request.args['candidate'], electionData), c=request.args['candidate'],
            repNum=get_party("Republican", electionData), demNum=get_party("Democrat", electionData), Num=get_party("N/A", electionData),
            repNumVote=get_party_vote("Republican", electionData),demNumVote=get_party_vote("Democrat", electionData),
            NumVote=get_party_vote("N/A", electionData))
        else:
            return render_template('Political_Demographic_Dropdown.html', candidate=get_candidate_options(electionData),
            repNum=get_party("Republican", electionData), demNum=get_party("Democrat", electionData),
            Num=get_party("N/A", electionData), repNumVote=get_party_vote("Republican", electionData),
            demNumVote=get_party_vote("Democrat", electionData), NumVote=get_party_vote("N/A", electionData),
            dDataPoints=get_cand_vote_data("Democrat", election_data), rDataPoints=get_cand_vote_data("Republican", election_data))

def get_cand_vote_data(party, election_data):
    candidate = []
    print(election_data)
    for data in election_data:
        print(data["Vote Data"])
        for a in data["Vote Data"].keys():
            print(data["Vote Data"][a]["Party"])
            if data["Vote Data"][a]["Party"] == party:
                # a not in candidate and
                candidate.append(a)

    print(party)
    print(candidate)
    options = ""
    for data in candidate:
        options = options + \
            Markup("{ x: new Date(" + data + "), y:" + data["Number of Votes"] + "},")
    options = options[:-1]
    print(options)
    return options

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
    return options

def political_party(candidate_chosen, election_data):
    political_party = ""
    key = "Political Party: "
    for data in election_data:
        for a in data["Vote Data"]:
            if a == candidate_chosen:
                political_party = data["Vote Data"][a]["Party"]

    return key + str(political_party)

def get_party(party_type, election_data):
    party = []
    count = 0
    for data in election_data:
        for a in data["Vote Data"]:
            if a not in party and data["Vote Data"][a]["Party"] == party_type:
                count+=1
                party.append(a)
    return count

def get_party_vote(party_type, election_data):
    num_votes = 0
    for data in election_data:
        for a in data["Vote Data"]:
            if data["Vote Data"][a]["Party"] == party_type:
                num_votes += data["Vote Data"][a]["Number of Votes"]
    return num_votes



if __name__ == "__main__":
    app.run(debug=True)
