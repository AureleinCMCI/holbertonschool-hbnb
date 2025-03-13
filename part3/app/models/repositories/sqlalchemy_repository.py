class SQLAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def add(self, obj):
        self.session.add(obj)

    def get(self, model, obj_id):
        return self.session.query(model).get(obj_id)

    def delete(self, obj):
        self.session.delete(obj)

    def save(self):
        self.session.commit()
