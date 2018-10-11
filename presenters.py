"""
    Presenters format the results to be answered as a JSON by the REST-API
"""
class PredictionPresenter():
    def __init__(self, prediction):
        self.prediction = prediction

    def to_dict(self):
        return {
            'probability': self.prediction.proba,
            'status': self.prediction.status,
            'label': self.prediction.label,
            'result': self.prediction.result,
            'bbox': self.prediction.bbox,
            'algorithm': {
                'href': '/v1/algorithm/' + self.prediction.algorithm.name + '?version=' + self.prediction.algorithm.version,
                'rel': 'algorithm',
                'type': 'GET'
            },
            'picture': {
                'href': '/v1/picture/' + self.prediction.picture.image_id,
                'rel': 'picture',
                'type': 'GET'
            }
        }


class PredictionsPresenter():
    def __init__(self, predictions):
        self.predictions = predictions

    def to_dict(self):
        return list(map(lambda p: PredictionPresenter(p).to_dict(), self.predictions))


class PicturePresenter():
    def __init__(self, picture):
        self.picture = picture

    def to_dict(self):
        return {
            'image_path': self.picture.image_path,
            'image_id': self.picture.image_id,
        }


class AlgorithmPresenter():
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def to_dict(self):
        return {
            'name': self.algorithm.name,
            'version': self.algorithm.version,
        }
