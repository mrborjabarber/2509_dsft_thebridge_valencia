
from flask import Flask,jsonify
from data.datos_dummy import books

application = Flask(__name__)

@application.route('/')
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@application.route('/api/v1/resources/books/all', methods=['GET'])
def get_all():
    # Para pasar a un json, que es lo que devuelve la API
    return jsonify(books)



app = application

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #application.debug = True
    application.run()

