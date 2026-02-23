from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from pydantic import BaseModel, Field
from datetime import datetime

from dotenv import load_dotenv
import bcrypt

from model.sql_handle import *
from crypto.eth import CryptoHandle

class EthTransferInfo(BaseModel):
    transfer_amount: int = Field(nullable=False)
    from_address: int = Field(nullable=False)
    time_stamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class UserSignUp(BaseModel):
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)

app = FastAPI()
crypto = CryptoHandle()
sql = SqlHandle()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Helper Function only to be run in post rquests
def get_user_obj(username):
    try:
        user_obj = sql.match_string(Users, Users.username, username)

    except ValueError:
        raise HTTPException(status_code=400, detail="User not found")

    return user_obj 

def hash_password(pasw):
    s = bcrypt.gensalt()
    h = bcrypt.hashpw(pasw.encode('utf-8'), s)

    return h.decode('utf-8')

def verify_password(pasw, pasw_hash):
    return bcrypt.checkpw(pasw.encode('utf-8'), pasw_hash.encode('utf-8'))

def decode_token(token):
    return get_user_obj(token)

def get_curr_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@app.on_event("startup")
def on_startup():
    sql.start_DB()
    sql.init_db_tables()

    load_dotenv()
    crypto.set_private_key()

@app.post("/token")
async def log_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Get the user object
    user = get_user_obj(form_data.username)

    # Hash the password and compare if true than return the bearer
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="incorrect Password")

    return {"access_token": user.username, "token_type": "bearer"}



# constrcuts a pending status
# A worker thread will poll it noticing when money is recieved
@app.post("/transactions")
async def createTransaction(eth_transfer: EthTransferInfo, curr_user: Annotated[Users, Depends(get_curr_user)]):
    transfer_dict = eth_transfer.model_dump()
    # Generate to address
    to_address = crypto.generate_address()

    # Get the current User using OAUTH 
    trans = Transaction(
        user_id = curr_user.id,
        amount = transfer_dict["transfer_amount"],
        from_address = transfer_dict["from_address"],
        to_address = to_address,
        time_stamp = transfer_dict["time_stamp"],
        status = "Pending",
    )
    
    sql.push_to_table(trans)
    sql.commit()
    
    return {}

@app.post("/sign_up")
async def sign_up(new_user: UserSignUp):
    try:
        old_user = get_user_object(new_user.username)
        
        if old_user:
            raise HTTPException(status_code=400, detail="User already exists")

    except:
        pass # This occours when theres no user so we want to be here!

    user_dict = new_user.model_dump()
    password_hash = hash_password(user_dict["password"])

    new_user_obj = Users(
        username = user_dict["username"],
        password_hash = password_hash
    )

    sql.push_to_table(new_user_obj)
    sql.commit()

    return {}
