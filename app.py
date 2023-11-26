from flask import Flask, request, make_response, jsonify
from firebase_admin import initialize_app, credentials, firestore
from firebaseConfig import FirebaseConfig
from datetime import datetime

cred = credentials.Certificate(FirebaseConfig)
initialize_app(cred)

db = firestore.client()

app = Flask(__name__)


@app.route('/seasons/', defaults={'season': ''})
@app.route('/seasons/<string:season>', methods=['GET'])
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


@app.route('/seasons', methods=['POST'])
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


# function that returns date and time DD/MM/YYYY - 00:00
def currentDateTime():
    cDate = datetime.now()
    string_date = '{:0>2}/{:0>2}/{} - {:0>2}:{:0>2}'.format(
        cDate.day, cDate.month, cDate.year,
        cDate.hour, cDate.minute)
    return str(string_date)  # DD/MM/YYYY - 00:00


if __name__ == '__main__':
    app.run()
