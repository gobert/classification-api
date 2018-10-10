import os
from application import Application
app = Application.get_instance('test')
app.init_db()
from classification_api import Picture


class TestPicture():
    def test_picture_init(self):
        assert Picture(image_id='foo').image_id == 'foo'

    def test_picture_create(self):
        assert Picture.create(image_id='foo').image_id == 'foo'
