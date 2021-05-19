from html_parse import db, Base, session


class Main(Base):
    """Основная таблица, содержит два поля: ``id`` и ``link``"""

    __tablename__ = "main"
    __bind_key__ = "engine"

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    link = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"you can get the atrubutes by id: {self.id}"

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise