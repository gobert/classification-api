from application import Application
import sqlalchemy
import datetime

app = Application.get_instance()


class Picture(app.Base):
    __tablename__ = 'pictures'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    image_id = sqlalchemy.Column(sqlalchemy.String(255))
    image_path = sqlalchemy.Column(sqlalchemy.String(1024))

    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime())

    def __init__(self, image_id=None):
        self.image_id = image_id

    @classmethod
    def create(cls, image_id=None):
        record = cls(image_id=image_id)
        record.created_at = datetime.datetime.now()
        record.updated_at = datetime.datetime.now()

        app.db_session.add(record)
        app.db_session.commit()

        return record
