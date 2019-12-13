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
        demColors = ["#37c732", "#43bfe6", "#4141f0"]
        repColors = ["#ff0400", "#ff4400", "#ff0077", "#ff01dd", "#ff015a", "#a601ff","#ff9a4d", "#ffc74d", "#ff6e4d", "#ea80ff", "#aa80ff"]
        if 'candidate' in request.args:
            return render_template('Political_Demographic_Dropdown.html', candidate=get_candidate_options(electionData),
            c_info=political_party(request.args['candidate'], electionData), c=request.args['candidate'],
            repNum=get_party("Republican", electionData), demNum=get_party("Democrat", electionData), Num=get_party("N/A", electionData),
            repNumVote=get_party_vote("Republican", electionData),demNumVote=get_party_vote("Democrat", electionData),
            NumVote=get_party_vote("N/A", electionData), dDataPoints=get_cand_vote_data("Democrat", electionData, demColors),
            rDataPoints=get_cand_vote_data("Republican", electionData, repColors))
        else:
            return render_template('Political_Demographic_Dropdown.html', candidate=get_candidate_options(electionData),
            repNum=get_party("Republican", electionData), demNum=get_party("Democrat", electionData),
            Num=get_party("N/A", electionData), repNumVote=get_party_vote("Republican", electionData),
            demNumVote=get_party_vote("Democrat", electionData), NumVote=get_party_vote("N/A", electionData),
            dDataPoints=get_cand_vote_data("Democrat", electionData, demColors),
            rDataPoints=get_cand_vote_data("Republican", electionData, repColors))


@app.route("/State")
def state():
    with open('Primary_Elections_2016.json') as election_data:
        electionData = json.load(election_data)
        if 'state' in request.args:
            return render_template('Political_Demographic_States.html', state=get_states(electionData), s=request.args['state'])
        else:
            return render_template('Political_Demographic_States.html', state=get_states(electionData))

def get_states(election_data):
    state = []
    for data in election_data:
        if data["Location"]["State"] not in state:
            state.append(data["Location"]["State"])
    options = ""
    for data in state:
        options = options + \
            Markup("<option value=\"" + data + "\">" + data + "</option>")
    return options


def get_cand_vote_data(party, election_data, colors):
    candidate = {}
    count = 0
    for data in election_data:
        for a in data["Vote Data"].keys():
            if data["Vote Data"][a]["Party"] == party:
                if a not in candidate:
                    candidate[a] = data["Vote Data"][a]["Number of Votes"]
                else:
                    candidate[a] += data["Vote Data"][a]["Number of Votes"]
    options = ""
    for data in candidate:
        options = options + \
            Markup('{ label: ("' + data + '"), y:' + str(candidate[data]) + ', color: ("' + colors[count] + '")'"},")
        count += 1
    options = options[:-1]
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
