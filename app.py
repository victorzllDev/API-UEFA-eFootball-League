from flask import Flask, request, make_response, jsonify
from firebase_admin import initialize_app, credentials, firestore
from firebaseConfig import FirebaseConfig

cred = credentials.Certificate(FirebaseConfig)
initialize_app(cred)

db = firestore.client()

app = Flask(__name__)


@app.route('/seasons/', defaults={'season': ''})
@app.route('/seasons/<string:season>', methods=['GET'])
def getSeasons(season):
    # checks if any value passes in the route.
    if season != '':
        collections = db.collection("seasons").document(season).collections()
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


if __name__ == '__main__':
    app.run()
