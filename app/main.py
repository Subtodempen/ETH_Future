from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

from dotenv import load_dotenv 

from model.sql_handle import *
from crypto.eth import CryptoHandle

class EthTransferInfo(BaseModel):
    TransferAmount: float
    FromAddress: int
    TimeStamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    UserID: int | None = Field(default=None)

app = FastAPI()
crypto = CryptoHandle()


@app.on_event("startup")
def on_startup():
    init_db_tables()
    load_dotenv()
    crypto.set_private_key()

# constrcuts a pending status
# A worker thread will poll it noticing when money is recieved
@app.post("/transactions")
async def createTransaction(eth_transfer: EthTransferInfo):
    transfer_dict = eth_transfer.model_dump()

    # Generate to address
    to_address = crypto.generate_address() 
    
    trans = Transaction(
        Amount = transfer_dict.TransferAmount,
        FromAddress = transfer_dict.FromAddress,
        ToAddress = to_address,
        TimeStamp = transfer_dict.TimeStamp,
        Status = "Pending",
    )
    
    with Session(engine) as session:
        session.add(trans)
        session.commit()

    return None
