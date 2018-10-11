from application import Application
from data_models import Prediction, Picture, Algorithm
from presenters import PredictionPresenter, PredictionsPresenter, PicturePresenter, AlgorithmPresenter
from flask import Flask, request, jsonify


flask_app = Flask(__name__)
app = Application.get_instance()


@flask_app.route('/')
def root():
    return jsonify({
        'links': [
            '/',
            '/_/health',
            '/v1/picture/<picture_id>',
            '/v1/algorithm/<name>?version=<version>',
            '/v1/predictions/<picture_id>',
            '/v1/predictions/weak'
        ]
    })


@flask_app.route('/_/health')
def health():
    return jsonify({
        'status': 'OK',
        'version': app.version(),
        'postgreSQL': app.postgresql_status()
    })


@flask_app.route('/v1/picture/<picture_id>')
def picture(picture_id):
    picture = Picture.find_by(image_id=picture_id)
    return jsonify(PicturePresenter(picture).to_dict())


@flask_app.route('/v1/algorithm/<name>')
def algorithm(name):
    version = request.args.get('version')
    algorithm = Algorithm.find_by(name=name, version=version)
    return jsonify(AlgorithmPresenter(algorithm).to_dict())


@flask_app.route('/v1/predictions/<image_id>')
def predictions(image_id):
    prediction = Prediction.find_by(picture_id=image_id)
    return jsonify(PredictionPresenter(prediction).to_dict())


@flask_app.route('/v1/predictions/weak')
def predictions_weak():
    predictions = Prediction.weak()
    return jsonify(PredictionsPresenter(predictions).to_dict())
