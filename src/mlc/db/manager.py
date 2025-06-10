from sqlmodel import create_engine, Session, SQLModel


class DbManager:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(self.db_url, echo=True)
        # Create tables
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        # Create session
        yield Session(self.engine)
