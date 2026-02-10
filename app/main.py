ifrom fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from model.sql_handle import init_db_tables


class EthTransferInfo(BaseModel):
    TransferAmount: float
    FromAddress: int
    TimeStamp: datetime
    UserID: int | None

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db_tables()
    

# constrcuts a pending status
# A worker thread will poll it noticing when money is recieved
@app.post("/transactions")
async def createTransaction(eth_transfer: EthTransferInfo):
    transfer_dict = eth_transfer.model_dump()
    
    trans = Transaction(
        Amount = transfer_dict.TransferAmount,
        FromAddress = transfer_dict.FromAddress,
        TimeStamp = transfer_dict.TimeStamp,
    )
