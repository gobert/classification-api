import os
import sqlalchemy

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.functions import create_database


class Application:
    # Here will be the singleton instance stored.
    __instance = None

    @staticmethod
    def get_instance(environment='development'):
        """ Static access method. """
        if Application.__instance is None:
            Application.__instance = Application(environment)
        return Application.__instance

    def __init__(self, environment):
        if 'FLASK_ENV' in os.environ:
            self.environment = os.environ['FLASK_ENV']
        else:
            self.environment = environment

        self.db_name = 'classification_api_%s' % self.environment
        self.db_url = 'postgresql://postgres:postgres@postgres:5432/%s' % self.db_name
        self.engine = sqlalchemy.create_engine(
            self.db_url,
            convert_unicode=True
        )
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                      autoflush=False,
                                                      bind=self.engine))
        self.Base = declarative_base()
        self.Base.query = self.db_session.query_property()

    def init_db(self):
        # import all modules here that might define models so that
        # they will be registered properly on the metadata.  Otherwise
        # you will have to import them first before calling init_db()
        try:
            from classification_api import Picture, Algorithm, Prediction
            self.Base.metadata.create_all(bind=self.engine)
        except sqlalchemy.exc.OperationalError as e:
            # create DB if it does not exist
            db_not_exist = ('FATAL:  database "%s" does not exist' % self.db_name in str(e))
            if db_not_exist:
                create_database(self.db_url)
                self.Base.metadata.create_all(bind=self.engine)
            else:
                raise e
