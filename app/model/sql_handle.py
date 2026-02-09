from sqlmodel import Field, SQLModel, create_engine


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

class TransactionTable(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    txHash: str
    FromAddress: str
    ToAddress: str
    Value: int
    Status: str



postgres_file_name = "database.db"
postgres_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(postgres_url, echo=True)

def init_db_tables():
    SQLModel.metadata.create_all(engine)
