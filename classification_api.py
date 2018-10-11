from application import Application
import datetime

from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


app = Application.get_instance()


class Picture(app.Base):
    """
        Represents a picture in the databse. On this pictures will algorithmes
        tested on to recognize if the product is good or defect.
    """
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True)
    predictions = relationship('Prediction', back_populates='picture')

    image_id = Column(String(255), index=True)
    image_path = Column(String(1024))

    created_at = Column(DateTime())
    updated_at = Column(DateTime())

    def __init__(self, image_id=None, image_path=None):
        self.image_id = image_id
        self.image_path = image_path

    @classmethod
    def create(cls, image_id=None, image_path=None):
        record = cls(image_id=image_id, image_path=image_path)
        record.created_at = datetime.datetime.now()
        record.updated_at = datetime.datetime.now()

        app.db_session.add(record)
        app.db_session.commit()

        return record


class Algorithm(app.Base):
    """
        Represents an predictive model algorithm on the computer. Those
        algorithm will predict if pictures represents a good or defect product.
    """
    __tablename__ = 'algorithms'

    id = Column(Integer, primary_key=True)
    predictions = relationship('Prediction', back_populates='algorithm')

    name = Column(String(255), index=True)
    version = Column(String(255), index=True)

    created_at = Column(DateTime())
    updated_at = Column(DateTime())

    def __init__(self, name=None, version=None):
        self.name = name
        self.version = version

    @classmethod
    def create(cls, name=None, version=None):
        record = cls(name=name, version=version)
        record.created_at = datetime.datetime.now()
        record.updated_at = datetime.datetime.now()

        app.db_session.add(record)
        app.db_session.commit()

        return record


class Prediction(app.Base):
    """
        Represent the outcome of an algorihm on a picture.
    """
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True)

    proba = Column(Float(), index=True)
    label = Column(String(255))
    result = Column(String(255))
    bbox = Column(ARRAY(Float))

    created_at = Column(DateTime())
    updated_at = Column(DateTime())

    algorithm_id = Column(Integer, ForeignKey('algorithms.id'), index=True)
    algorithm = relationship('Algorithm', back_populates='predictions')
    picture_id = Column(Integer, ForeignKey('pictures.id'), index=True)
    picture = relationship('Picture', back_populates='predictions')

    def __init__(self, proba=None, label=None, result=None, bbox=None, algorithm_id=None, picture_id=None):
        self.proba = proba
        self.label = label
        self.result = result
        self.bbox = bbox
        self.algorithm_id = algorithm_id
        self.picture_id = picture_id

    @classmethod
    def create(cls, proba=None, label=None, result=None, bbox=None, algorithm_id=None, picture_id=None):
        record = cls(proba=proba, label=label, result=result, bbox=bbox, algorithm_id=algorithm_id, picture_id=picture_id)
        record.created_at = datetime.datetime.now()
        record.updated_at = datetime.datetime.now()

        app.db_session.add(record)
        app.db_session.commit()

        return record
