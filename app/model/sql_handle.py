from sqlmodel import create_engine, Session, select

class SqlHandle():
    def __init__(self, postgres_url):        
        self.engine = create_engine(postgres_url, echo=True)
        self.session = Session(self.engine) # Change this make temporary

    def set_db_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def push_to_table(self, table_row):
        self.session.add(table_row)

    def commit(self):
        self.session.commit()

    def match_string(self, table, table_val, str):
        statement = select(table).where(table_val == str)
        obj = self.session.exec(statement).first()

        if obj is None:
            raise ValueError("No Object in db")

        return obj
    
    
