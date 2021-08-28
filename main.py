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
import sqlalchemy.exc
import sqlmodel
from pydantic import SecretStr
from sqlmodel import Field

logging.basicConfig(level=logging.DEBUG)
LOGGGER = logging.getLogger("got-api")


# Config


class _Config(pydantic.BaseSettings):
    conn_str: str
    client_id: str
    client_secret: SecretStr
    refresh_on_startup: bool = False


@functools.lru_cache(maxsize=1)
def get_config(_env_file=".env", **kwargs) -> _Config:
    config = _Config(_env_file=_env_file, **kwargs)
    LOGGGER.debug(pf(config))
    return config


# #############################################################################

# Models


class House(sqlmodel.SQLModel, table=True):
    name: str = Field(primary_key=True)
    words: Optional[str] = None


class Character(sqlmodel.SQLModel, table=True):
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

# Database

ENGINE = sqlmodel.create_engine(get_config().conn_str)


def db_session() -> sqlmodel.Session:
    with sqlmodel.Session(ENGINE) as session:
        yield session


def all_houses(session: sqlmodel.Session = fastapi.Depends(db_session)):
    return session.exec(sqlmodel.select(House)).all()


# #############################################################################


# API tasks


def from_csv(model: sqlmodel.SQLModel, path: pathlib) -> List[sqlmodel.SQLModel]:
    with open(path, mode="r") as csv_file:
        return [model.parse_obj(row) for row in csv.DictReader(csv_file)]


def cleanup():
    LOGGGER.info("cleaning up ...")
    if not get_config().refresh_on_startup:
        return
    sqlmodel.SQLModel.metadata.drop_all(ENGINE)
    LOGGGER.info("All Tables dropped")


def startup():
    LOGGGER.info("Starting up ...")
    sqlmodel.SQLModel.metadata.create_all(ENGINE)

    data_dir = pathlib.Path.cwd() / "data"
    if not get_config().refresh_on_startup:
        return cleanup()
    LOGGGER.info("Seeding data ...")
    with sqlmodel.Session(ENGINE) as session:
        session.add_all(from_csv(House, data_dir / "houses.csv"))
        session.commit()


# #############################


# API Configuration

API_VERSION = "0.0.1a"

API = fastapi.FastAPI(
    title="GOT Characters",
    description="Spoiler free Game of Thrones Characters API.",
    version=API_VERSION,
    on_startup=[startup],
    on_shutdown=[cleanup],
)


# #############################################################################

# Error Handlers


@API.exception_handler(sqlalchemy.exc.OperationalError)
async def handle_db_error(
    request: fastapi.Request, exc: sqlalchemy.exc.OperationalError
):
    LOGGGER.exception(exc)
    return fastapi.responses.JSONResponse(
        status_code=500, content={"detail": "Database Error"}
    )


# Controllers


@API.get("/houses", response_model=List[House])
async def get_houses(houses=fastapi.Depends(all_houses)):
    return houses
