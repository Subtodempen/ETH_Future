from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime

class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password_hash: str
    balance: int = Field(default=0)
    pending_balance: int = Field(default=0)
    
class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    price: int
    future_price: int
    time_placed: str
    expeiry: str
    status: str

class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    tx_hash: str | None = Field(default = None)
    time_stamp: datetime
    from_address: str
    bip44_index: int
    amount: int
    status: str


class SqlHandle():
    def __init__(self):
        self.postgres_url = "postgresql://postgres:root@localhost:5432/database"

    def start_DB(self):
        self.engine = create_engine(self.postgres_url, echo=True)
        self.session = Session(self.engine)

    def init_db_tables(self):
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
    
    
