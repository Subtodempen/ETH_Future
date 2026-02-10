from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    Balance: int
    PendingBalance: int
    
class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    UserId: int = Field(index=True)
    Price: int
    FuturePrice: int
    TimePlaced: str
    Expeiry: str
    Status: str

class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    UserId: int = Field(index=true)
    txHash: str | None = Field(default = None)
    FromAddress: str
    ToAddress: str
    TimeStamp: datetime.datetime
    Amount: int
    Status: str


postgres_url = "postgresql://postgres:root@localhost:5432/database"
engine = create_engine(postgres_url, echo=True)

def init_db_tables():
    SQLModel.metadata.create_all(engine)
