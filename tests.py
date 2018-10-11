import os
from application import Application
app = Application.get_instance('test')
app.init_db()
from classification_api import Picture, Algorithm, Prediction
import pytest
from freezegun import freeze_time
import datetime


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
