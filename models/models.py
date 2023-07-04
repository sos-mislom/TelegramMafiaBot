from abstract_models.abstract_models import *
from db import get_db
from typing import Optional


class User(AbstractModel):
    database = get_db()
    user_id: Optional[int]
    second_name: Optional[str]
    circles: Optional[str]

    TABLE_NAME = 'users'

class Greetings(AbstractModel):
    database = get_db()
    user_id: Optional[int]
    text: Optional[str]

    TABLE_NAME = 'greetings'


