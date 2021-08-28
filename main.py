"""
GOT-CHAR main.py
~~~~~~~~~~~~~~~

Nouns
-----
    Locale
    Death
    Character
    Houses
    Book
"""
import csv
import functools
import logging
import pathlib
from pprint import pformat as pf
from typing import List, Optional

import fastapi
import pydantic
import sqlmodel
from pydantic import SecretStr
from sqlmodel import Field, SQLModel

logging.basicConfig(level=logging.INFO)
LOGGGER = logging.getLogger("got-api")

# Models


class House(SQLModel, table=True):
    name: str = Field(primary_key=True)
    words: Optional[str] = None


class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: Optional[str] = None
    house: Optional[str]
    title: Optional[str] = None
    sex: str
    father: Optional[str] = None
    mother: Optional[str] = None
    Liege: Optional[str] = None


# #############################################################################

# Config


class _Config(pydantic.BaseSettings):
    conn_str: str
    client_id: str
    client_secret: SecretStr
    refresh_on_startup: bool = True


@functools.lru_cache(maxsize=1)
def get_config(_env_file=".env", **kwargs) -> _Config:
    return _Config(_env_file=_env_file, **kwargs)


ENGINE = sqlmodel.create_engine(get_config().conn_str)


# API tasks


def from_csv(model: sqlmodel.SQLModel, path: pathlib) -> List[sqlmodel.SQLModel]:
    with open(path, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        LOGGGER.info(reader)
        LOGGGER.info(csv.list_dialects())
        LOGGGER.info(pf([x for x in reader]))
        models = [model.parse_obj(row) for row in reader]
        LOGGGER.info(pf(models))
        return models


def seed_all_data():
    data_dir = pathlib.Path.cwd() / "data"
    if not get_config().refresh_on_startup:
        return
    with sqlmodel.Session(ENGINE) as session:
        session.add_all(from_csv(House, data_dir / "houses.csv"))


# #############################


# API Configuration

API_VERSION = "0.0.1a"

API = fastapi.FastAPI(
    title="GOT Characters",
    description="Spoiler free Game of Thrones Characters API.",
    version=API_VERSION,
    on_startup=[seed_all_data],
)


# #############################################################################


@API.get("/houses")
async def get_houses():
    pass
