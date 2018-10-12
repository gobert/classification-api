import os
from application import Application
app = Application.get_instance('test')
app.drop_db_if_exist()
app.init_db()
from data_models import Picture, Algorithm, Prediction
from controllers import flask_app
import pytest
from freezegun import freeze_time
import datetime
import tempfile
import json


class TestPicture():
    @pytest.fixture
    def image_id(self):
        return '234567890'

    @pytest.fixture
    def image_path(self):
        return '20181011/234567890.jpg'

    def test_picture_init(self, image_id):
        assert Picture(image_id=image_id).image_id == image_id

    def test_picture_create_image_id(self, image_id):
        assert Picture.create(image_id=image_id).image_id == image_id

    def test_picture_create_image_path(self, image_path):
        assert Picture.create(image_path=image_path).image_path == image_path

    def test_picture_create_created_at(self):
        now = freeze_time('2018-10-11 11:26:01')
        now.start()
        assert Picture.create().created_at ==datetime.datetime(2018, 10, 11, 11, 26, 1)
        now.stop()

    def test_find_by(self, image_id, image_path):
        Picture.create(image_id=image_id, image_path=image_path)
        assert Picture.find_by(image_id=image_id).image_id == image_id


class TestAlgorithm():
    @pytest.fixture
    def name(self):
        return 'DeevioNet'

    @pytest.fixture
    def version(self):
        return '1.0'

    def test_algorithm_init(self, name):
        assert Algorithm(name=name).name == name

    def test_algorithm_create_name(self, name):
        assert Algorithm.create(name=name).name == name

    def test_algorithm_create_version(self, version):
        assert Algorithm.create(version=version).version == version


class TestPrediction():
    # algorithm_id = Column(Integer, ForeignKey('algorithms.id'))
    # picture_id = Column(Integer, ForeignKey('pictures.id'))

    @pytest.fixture
    def proba(self):
        return 0.99999

    @pytest.fixture
    def label(self):
        return 'nails'

    @pytest.fixture
    def bbox(self):
        return [1008.8, 280.6, 1110.0, 380.72021484375]

    @pytest.fixture
    def result(self):
        return 'good'

    def test_prediction_init(self, label):
        assert Prediction(label=label).label == label

    def test_prediction_create_proba(self, proba):
        assert Prediction.create(proba=proba).proba == proba

    def test_prediction_create_bbox(self, bbox):
        assert Prediction.create(bbox=bbox).bbox == bbox

    def test_prediction_create_result(self, result):
        assert Prediction.create(result=result).result == result

    def test_prediction_create_algorithm(self):
        algorithm = Algorithm.create()
        prediction = Prediction.create(algorithm_id=algorithm.id)
        assert prediction.algorithm == algorithm
        assert algorithm.predictions[-1] == prediction

    def test_prediction_create_picture(self):
        picture = Picture.create()
        prediction = Prediction.create(picture_id=picture.id)
        assert prediction.picture == picture
        assert picture.predictions[-1] == prediction

    def test_prediction_create_from_mq(self):
        payload = '{"algorithm": {"name": "DeevioNet","version": "1.0"},"status":"complete","imagePath":"20180907/1536311270718.jpg","imageId":"1536311270718","output":[{"bbox":[1008.8831787109375,280.6226501464844,1110.0245361328125,380.72021484375],"probability":0.9725130796432495,"label":"nail","result":"good"} ]}'
        Prediction.create_from_mq(payload)


class TestControllers():
    @pytest.fixture
    def client(self):
        flask_app.config['TESTING'] = True
        client = flask_app.test_client()
        yield client

    def test_root(self, client):
        rv = client.get('/')
        links = json.loads(rv.data)['links']
        assert links[0] == '/'
        assert links[1] == '/_/health'
        assert links[2] == '/v1/picture/<picture_id>'
        assert links[3] == '/v1/algorithm/<name>?version=<version>'
        assert links[4] == '/v1/predictions/<picture_id>'
        assert links[5] == '/v1/predictions/weak'

    def test_health(self, client):
        rv = client.get('/_/health')
        body = json.loads(rv.data)
        assert body['status'] == 'OK'
        assert body['version'] == app.version()

    def test_get_picture(self, client):
        picture = Picture.create(image_path='20181012/foobar.jpg', image_id='foobar.jpg')
        body = json.loads(client.get('/v1/picture/%s' % picture.image_id).data)
        assert body['image_path'] == '20181012/foobar.jpg'
        assert body['image_id'] == 'foobar.jpg'

    def test_get_algorithm(self, client):
        algorithm = Algorithm.create(name='DeevioNet', version='1.1')
        body = json.loads(client.get('/v1/algorithm/' + algorithm.name + '?version=' + algorithm.version).data)
        assert body['name'] == 'DeevioNet'
        assert body['version'] == '1.1'

    def test_predictions_by_image_id(self, client):
        picture = Picture.create(image_id='foobar.jpg')
        algorithm = Algorithm.create(name='DeevioNet', version='1.1')
        prediction = Prediction.create(picture_id=picture.id, algorithm_id=algorithm.id, proba=0.99, status='complete', label='nail', result='good', bbox=[100, 200, 500, 500])

        body = json.loads(client.get('/v1/predictions/%s' % picture.id).data)

        assert body['probability'] == prediction.proba
        assert body['status'] == prediction.status
        assert body['label'] == prediction.label
        assert body['result'] == prediction.result
        assert body['bbox'] == prediction.bbox
        assert body['algorithm']['type'] == 'GET'
        assert body['algorithm']['rel'] == 'algorithm'
        assert body['algorithm']['href'] == '/v1/algorithm/DeevioNet?version=1.1'
        assert body['picture']['type'] == 'GET'
        assert body['picture']['rel'] == 'picture'
        assert body['picture']['href'] == '/v1/picture/foobar.jpg'

    def test_predictions_weak(self, client):
        picture = Picture.create(image_id='foobar.jpg')
        algorithm = Algorithm.create(name='DeevioNet', version='1.1')
        prediction = Prediction.create(picture_id=picture.id, algorithm_id=algorithm.id, proba=0.69)
        prediction = Prediction.create(picture_id=picture.id, algorithm_id=algorithm.id, proba=0.7)

        body = json.loads(client.get('/v1/predictions/weak').data)

        assert len(body) == 1
