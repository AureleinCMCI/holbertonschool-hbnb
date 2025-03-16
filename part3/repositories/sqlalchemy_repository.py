from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class SQLAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def create(self, obj):
        self.session.add(obj)
        self.session.commit()

    def read(self, model, obj_id):
        return self.session.query(model).get(obj_id)

    def update(self, obj):
        self.session.merge(obj)
        self.session.commit()

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()
