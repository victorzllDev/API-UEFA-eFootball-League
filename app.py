from flask import Flask, request, make_response, jsonify
from firebase_admin import initialize_app, credentials, firestore
from firebaseConfig import FirebaseConfig
from datetime import datetime

cred = credentials.Certificate(FirebaseConfig)
initialize_app(cred)

db = firestore.client()

app = Flask(__name__)


@app.route('/seasons/', defaults={'season': ''})
@app.route('/seasons/<string:season>/', methods=['GET'])
def getSeasons(season):
    # checks if any value passes in the route.
    if season != '':
        collections = db.collection('seasons').document(season).collections()
        data = {}
        for collection in collections:
            collection_data = []

            for doc in collection.stream():
                collection_data.append(doc.to_dict())

            data[collection.id] = collection_data
        # returns the date of the season that came on the route
        if data:
            return make_response(jsonify(data))
        else:
            return make_response(jsonify({'error': 'season does not exist'}), 404)
    else:
        # returns existing routes
        docs = db.collection('seasons').stream()
        data = []
        for doc in docs:
            data.append(doc.id)
        return make_response(jsonify(data))


@app.route('/seasons/', methods=['POST'])
def postSeasons():
    nameSeason = request.json['season']
    # check if the name of the season was passed through json
    if nameSeason:
        # check if a session with the same name already exists.
        docs = db.collection('seasons').stream()
        for doc in docs:
            if nameSeason == doc.id:
                return make_response(jsonify({'error': 'There is already a session with the same name.'}), 404)
        # creating a document with the creation date
        date = currentDateTime()
        db.collection('seasons').document(
            nameSeason).set({'creation_date': date})
        return make_response(jsonify({'message': 'season created successfully.'}), 201)
    else:
        return make_response(jsonify({'error': 'the data in json did not come.'}), 404)


@app.route('/teams/', defaults={'season': '', 'teamId': ''}, methods=['GET'])
@app.route('/teams/<string:season>/', defaults={'teamId': ''}, methods=['GET'])
@app.route('/teams/<string:season>/<string:teamId>/', methods=['GET'])
def getTeams(season, teamId):
    if season:
        # rescuing all documents within the sub collection team
        doc_ref = db.collection('seasons').document(season)
        subcolecao_ref = doc_ref.collection('teams')
        documentos_subcolecao = subcolecao_ref.stream()
        # saving the values ​​in the data variable
        data = []
        for doc in documentos_subcolecao:
            data.append(doc.to_dict())
        # checking if the ID passed in the URL exists and returning an object if the value is valid
        if teamId:
            team = None
            for doc in data:
                if doc['id'] == teamId:
                    team = doc
            # checks if the item exists, and returns the item or error
            return make_response(jsonify(team)) if team else make_response(jsonify({'error': 'team not found'}), 404)
        else:
            return make_response(jsonify(data))
    else:
        return make_response(jsonify({'error': 'season not informed by the URL'}), 404)


@app.route('/teams/', defaults={'season': ''}, methods=['POST'])
@app.route('/teams/<string:season>/', methods=['POST'])
def postTeams(season):
    if season:
        req = request.json
        if req and type(req) == list:
            # looping through the teams array, and creating a document in the sub collection with the teams
            for team in req:
                teamId = db.collection('seasons').document(
                    season).collection('teams').add({})[1].id

                team.update({'id': teamId})

                db.collection('seasons').document(season).collection(
                    'teams').document(teamId).set(team)

            return make_response(jsonify({'messagem': 'successfully created teams'}), 201)
        else:
            return make_response(jsonify({'error': 'empty array'}), 404)
    else:
        return make_response(jsonify({'error': 'season not specified in route URL'}), 404)


@app.route('/matches/', defaults={'season': '', 'matcheId': ''}, methods=['GET'])
@app.route('/matches/<string:season>/', defaults={'matcheId': ''}, methods=['GET'])
@app.route('/matches/<string:season>/<string:matcheId>/', methods=['GET'])
def getMatches(season, matcheId):
    if season:
        # rescuing all documents within the sub collection team
        doc_ref = db.collection('seasons').document(season)
        subcollection_ref = doc_ref.collection('matches')
        documents_subcollection = subcollection_ref.stream()
        # saving the values ​​in the data variable
        data = []
        for doc in documents_subcollection:
            data.append(doc.to_dict())

        # checking if the ID passed in the URL exists and returning an object if the value is valid
        if matcheId:
            for matche in data:
                if matche['id'] == matcheId:
                    return make_response(jsonify(matche))

            return make_response(jsonify({'error': 'matche not found'}), 404)
        else:
            return make_response(jsonify(data))
    else:
        return make_response(jsonify({'error': 'season not present on the route'}), 404)


# function that returns date and time DD/MM/YYYY - 00:00
def currentDateTime():
    cDate = datetime.now()
    string_date = '{:0>2}/{:0>2}/{} - {:0>2}:{:0>2}'.format(
        cDate.day, cDate.month, cDate.year,
        cDate.hour, cDate.minute)
    return str(string_date)  # DD/MM/YYYY - 00:00


if __name__ == '__main__':
    app.run()
