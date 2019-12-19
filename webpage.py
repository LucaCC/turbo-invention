from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json
import random

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


@app.route("/Candidates")
def candidate():
    with open('Primary_Elections_2016.json') as election_data:
        electionData = json.load(election_data)
        if 'state' in request.args:
            return render_template('Political_Demographic_Candidates.html', party=get_party(electionData), p=request.args['party'])
        else:
            return render_template('Political_Demographic_Candidates.html', party=get_party(electionData))


@app.route("/State")
def state():
    with open('Primary_Elections_2016.json') as election_data:
        electionData = json.load(election_data)
        if 'state' in request.args:
            print(get_vote("Republican", "Mississippi", election_data))
            return render_template('Political_Demographic_States.html', state=get_states(electionData), s=request.args['state'],
            counties=get_counties(electionData, request.args['state']), dVote=Markup('{ label: "' + str(2) + '", y:' + str(3) + '}'),
            rVote=get_vote("Republican", request.args['state'], election_data))
        elif 'counties' in request.args:
            return render_template('Political_Demographic_States.html', state=get_states(electionData), c=request.args['counties'],
            counties=get_counties(electionData, request.args['state']), s=request.args['state'])
        else:
            return render_template('Political_Demographic_States.html', state=get_states(electionData))

def get_vote(party, state, election_data):
    candidate = {}
    for data in election_data:
        for a in data["Vote Data"].keys():
            # print(state, data["Location"]["State"])
            if data["Location"]["State"] == state and data["Vote Data"][a]["Party"] == party:
                if a not in candidate:
                    candidate[a] = data["Vote Data"][a]["Number of Votes"]
                else:
                    candidate[a] += data["Vote Data"][a]["Number of Votes"]
    options = ""
    for data in candidate:
        print(data, candidate[data])
        options = options + \
            Markup('{y:' + str(candidate[data]) + ', label: "' + data + '"},')
            # Markup('{y:' + str(candidate[data]) + ', label: "' + data + '",  color: "' + color_party(party) + '"},')
    options = options[:-1]
    return options

def color_party(party):
    r = 0
    b = 0
    c = 0
    if party == "Democratic":
        r = random.randint(0,50)
        g = random.randint(0,150)
        b = random. randint(200, 255)
    else:
        b = random.randint(0,50)
        g = random.randint(0,150)
        r = random. randint(200, 255)
    return "rgb(" +str(r) + ", " + str(g) + ", " + str(b) + ")"


def get_party(election_data):
    party = []
    for data in election_data:
        for a in data["Vote Data"].keys():
            if data["Vote Data"][a]["Party"] not in party:
                party.append(data["Vote Data"][a]["Party"])
    options = ""
    for data in party:
        options = options + \
            Markup("<option value=\"" + data + "\">" + data + "</option>")
    return options
def get_counties(election_data, state):
    counties = []

def get_states(election_data):
    states = []
    for data in election_data:
        if data["Location"]["State"] not in states:
            states.append(data["Location"]["State"])
    options = ""
    for data in states:
        options = options + \
            Markup("<option value=\"" + data + "\">" + data + "</option>")
    return options
def get_counties(election_data, state):
    counties = []
    for data in election_data:
        if data["Location"]["State"] == state and data["Location"]["County"] not in counties:
            counties.append(data["Location"]["County"])
    options = ""
    for data in counties:
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
