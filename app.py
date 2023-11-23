from flask import Flask, make_response, jsonify
from firebase_admin import initialize_app, credentials, firestore
from firebaseConfig import FirebaseConfig

cred = credentials.Certificate(FirebaseConfig)
initialize_app(cred)

db = firestore.client()

app = Flask(__name__)


@app.route("/seasons/", defaults={'season': 'none'})
@app.route("/seasons/<string:season>", methods=['GET'])
def getSeasons(season):
    # Fetching data from the database.
    docs = db.collection("seasons").stream()
    data = {}
    for doc in docs:
        data.update({doc.id: doc.to_dict()})

    # check if there is a date, and verify if a parameter is present in the URL.
    if data:
        if season != 'none':
            try:
                return make_response(jsonify(data[season]))
            except KeyError:
                return make_response(jsonify({'error': 'Unable to find season data'}), 404)
        else:
            return make_response(jsonify(data))
    else:
        return make_response(jsonify({'error': 'Unable to find data'}), 404)


if __name__ == '__main__':
    app.run()
