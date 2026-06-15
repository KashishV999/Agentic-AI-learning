
from pydantic import BaseModel
class GithubFile(BaseModel):
    owner: str
    repo: str
    path: str
    ref: str = "main"
    truncateValue: int = 1000
