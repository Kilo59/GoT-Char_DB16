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
import functools
import logging
from pprint import pformat as pf
from typing import List, Optional, Union

import fastapi
import pydantic
import sqlalchemy.engine
import sqlalchemy.exc
import sqlmodel
from fastapi import Depends, Query
from pydantic import AnyUrl, SecretStr
from sqlmodel import Field, SQLModel

import api.data

LOGGGER = logging.getLogger("got-api")

# Config


class _Config(pydantic.BaseSettings):
    database_url: Union[AnyUrl, str]
    client_id: str
    client_secret: SecretStr
    debug_mode: bool = False

    @pydantic.validator("database_url")
    def postgres_scheme(cls, v: str) -> str:
        if v.startswith("postgres://"):
            LOGGGER.warning("updating postgres connection string")
            return v.replace("postgres://", "postgresql://", 1)
        return v


@functools.lru_cache(maxsize=1)
def get_config(_env_file=".env", **kwargs) -> _Config:
    config = _Config(_env_file=_env_file, **kwargs)
    # NOTE: beware of exposing user:password in database_url
    LOGGGER.debug(pf(config))
    return config


DEBUG_MODE: bool = get_config().debug_mode
logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)

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


@functools.lru_cache(maxsize=1)
def get_engine(**config_kw) -> sqlalchemy.engine.Engine:
    config = get_config(**config_kw)
    return sqlmodel.create_engine(config.database_url, echo=config.debug_mode)


def create_db_and_tables():
    LOGGGER.info("creating databse and tables ...")
    SQLModel.metadata.create_all(get_engine(), checkfirst=True)


def db_session() -> sqlmodel.Session:
    with sqlmodel.Session(get_engine()) as session:
        yield session


def query_houses(
    session: sqlmodel.Session = Depends(db_session),
    limit: Optional[int] = None,
    skip: Optional[int] = None,
    name: Optional[str] = Query(None, description="`name` substring filter"),
    words: Optional[str] = Query(None, description="`words` substring filter"),
):
    statement = sqlmodel.select(House)
    if name:
        statement = statement.filter(House.name.contains(name))
    if words:
        statement = statement.filter(House.words.contains(words))
    return session.exec(statement.offset(skip).limit(limit)).all()


# #############################################################################


# API tasks


def cleanup():
    LOGGGER.info("cleaning up ...")
    sqlmodel.SQLModel.metadata.drop_all(get_engine())
    LOGGGER.info("All Tables dropped")


def startup(**config_kw):
    LOGGGER.info("Starting up ...")

    create_db_and_tables()

    LOGGGER.info("Seeding data ...")
    try:
        with sqlmodel.Session(get_engine(**config_kw)) as session:
            for i, model in enumerate(api.data.from_csv(House, api.data.HOUSES_CSV)):
                try:
                    session.add(model)
                    LOGGGER.info(f"{i} - {model.name} added")
                except sqlalchemy.exc.OperationalError as insert_err:
                    LOGGGER.info(f"{i} - {insert_err}")
            session.commit()
    except (sqlalchemy.exc.OperationalError, sqlalchemy.exc.IntegrityError) as db_err:
        LOGGGER.warning(f"{db_err.__class__.__name__} - Data may already exist")
        LOGGGER.warning(db_err)


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
    LOGGGER.info(f"{exc.__class__.__name__} - {request.url}")
    LOGGGER.exception(exc)
    return fastapi.responses.JSONResponse(
        status_code=500, content={"detail": "Database Error"}
    )


# Controllers


@APP.get("/houses", response_model=List[House])
async def get_houses(houses=Depends(query_houses)):
    return houses
