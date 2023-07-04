import ast
import datetime
import json
from contextlib import closing
from typing import List
from enum import Enum

class AbstractModel:
    TABLE_NAME = None
    
    SECRET_FIELDS = []

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, datetime.datetime):
                kwargs[k] = v.strftime('%d.%m.%Y %H:%M:%S')
        object.__setattr__(self, 'fields', kwargs)

    def __getattr__(self, item):
        return self.fields[item] if item in self.fields.keys() else None

    def __setattr__(self, key, value):
        self.fields[key] = value

    def update_fields(self, fields: dict):
        object.__getattribute__(self, 'fields').update(fields)

    def _get_keys(self):
        return f"({', '.join(self.fields.keys())})"

    def add(self):
        with closing(self.database.cursor()) as cur:
            data = ast.literal_eval(str(self.fields))
            values = ", ".join(f"'{data[s]}'" for s in data)
            sql = f'INSERT INTO {self.TABLE_NAME} {self._get_keys()} VALUES ({values})'
            print(sql)
            cur.execute(sql)
            self.database.commit()

    def get_one(self) -> bool:
        with closing(self.database.cursor()) as cur:
            sql = f"SELECT * FROM {self.TABLE_NAME}"
            data = ast.literal_eval(str(self.fields))
            if len(self.fields) > 0:
                sql += " WHERE " + str(' AND '.join(f"{k}='{data[k]}'" for k in data))
            cur.execute(sql)
            f = cur.fetchone()
            if f is not None:
                return True
        return False

    def get_many(self) -> List[__name__]:
        with closing(self.database.cursor()) as cur:
            sql = f"SELECT * FROM {self.TABLE_NAME}"
            data = ast.literal_eval(str(self.fields))
            if len(self.fields) > 0:
                sql += " WHERE " + str(' AND '.join(f"{k}='{data[k]}'" for k in data))
            models = [x for x in cur.execute(sql)]
        return models

    def update(self):
        with closing(self.database.cursor()) as cur:
            data = ast.literal_eval(str(self.fields))
            f = cur.execute(
                f"UPDATE {self.TABLE_NAME} SET " + ', '.join(
                    f"{k}='{data[k]}'" for k in data) + f" WHERE id = '{self.id}'"
            )
            self.database.commit()
            return f

    def delete(self):
        with closing(self.database.cursor()) as cur:
            data = ast.literal_eval(str(self.fields))
            f = cur.execute(
                f"DELETE FROM {self.TABLE_NAME}" +
                " WHERE " + str(' AND '.join(f"{k}='{data[k]}'" for k in data))
            )
            self.database.commit()
            return f

    def __str__(self):
        return str(self.serialize(include_secret_fields=True))

    def serialize(self, include_secret_fields=False):
        if include_secret_fields:
            return self.fields
        return {k: v for k, v in self.fields.items() if k not in self.SECRET_FIELDS}

    def to_json(self, **kwargs):
        return json.dumps(self.serialize(**kwargs))

class Action(str, Enum):
    anek = "anek"
    save_to_chat = "save_to_chat"
    find_anek_by_tags = "find_anek_by_tags"
    to_tell_anek = "to_tell_anek"
    reset_all_ban_words = "reset_all_ban_words"
    meme = "meme"
    strawberry = "strawberry"
