from pydantic import BaseModel


class ServerDetail(BaseModel):
    description: str
    photoURL: str
    emailAddress: str
