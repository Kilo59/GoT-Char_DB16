"""
GOT-CHAR api.main.py
~~~~~~~~~~~~~~~~~~~~

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
from typing import List, Optional, Union

import fastapi
import pydantic
import sqlalchemy.exc
import sqlmodel
from pydantic import AnyUrl, SecretStr
from sqlmodel import Field, SQLModel

logging.basicConfig(level=logging.DEBUG)
LOGGGER = logging.getLogger("got-api")

# Config


class _Config(pydantic.BaseSettings):
    database_url: Union[AnyUrl, str]
    client_id: str
    client_secret: SecretStr
    refresh_on_startup: bool = True

    @pydantic.validator("database_url")
    def postgres_scheme(cls, v: str) -> str:
        if v.startswith("postgres://"):
            LOGGGER.warning("updating postgres connection string")
            return v.replace("postgres://", "postgresql://", 1)
        return v


@functools.lru_cache(maxsize=1)
def get_config(_env_file=".env", **kwargs) -> _Config:
    config = _Config(_env_file=_env_file, **kwargs)
    LOGGGER.debug(pf(config))
    return config


# #############################################################################

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

# Database

DATABASE_URL = get_config().database_url
ENGINE = sqlmodel.create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    LOGGGER.info("creating databse and tables ...")
    SQLModel.metadata.create_all(ENGINE)


def db_session() -> sqlmodel.Session:
    with sqlmodel.Session(ENGINE) as session:
        yield session


def all_houses(
    session: sqlmodel.Session = fastapi.Depends(db_session),
    limit: Optional[int] = None,
    skip: Optional[int] = None,
):
    return session.exec(sqlmodel.select(House)).all()


# #############################################################################


# API tasks


def from_csv(model: sqlmodel.SQLModel, path: pathlib) -> List[sqlmodel.SQLModel]:
    with open(path, mode="r") as csv_file:
        return [model.parse_obj(row) for row in csv.DictReader(csv_file)]


def cleanup():
    LOGGGER.info("cleaning up ...")
    sqlmodel.SQLModel.metadata.drop_all(ENGINE)
    LOGGGER.info("All Tables dropped")


def startup():
    LOGGGER.info("Starting up ...")

    data_dir = pathlib.Path.cwd() / "data"

    LOGGGER.info("Seeding data ...")
    try:
        with sqlmodel.Session(ENGINE) as session:
            for i, model in enumerate(from_csv(House, data_dir / "houses.csv")):
                try:
                    session.add(model)
                    LOGGGER.info(f"{i} - {model.name} added")
                except sqlalchemy.exc.OperationalError as insert_err:
                    LOGGGER.info(f"{i} - {insert_err}")
            session.commit()
    except sqlalchemy.exc.OperationalError as db_err:
        LOGGGER.error(db_err)


# #############################


# API Configuration

API_VERSION = "0.0.1a"

APP = fastapi.FastAPI(
    title="GOT Characters",
    description="Spoiler free Game of Thrones Characters API.",
    version=API_VERSION,
    docs_url="/",
    redoc_url="/docs",
    on_startup=[startup],
)


# #############################################################################

# Error Handlers


@APP.exception_handler(sqlalchemy.exc.OperationalError)
async def handle_db_error(
    request: fastapi.Request, exc: sqlalchemy.exc.OperationalError
):
    LOGGGER.exception(exc)
    return fastapi.responses.JSONResponse(
        status_code=500, content={"detail": "Database Error"}
    )


# Controllers


@APP.get("/houses", response_model=List[House])
async def get_houses(houses=fastapi.Depends(all_houses)):
    return houses
