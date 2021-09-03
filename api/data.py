"""
api.data
~~~~~~~~
Methods for importing and parsing and data.
"""
import csv
import pathlib
from typing import List

from sqlmodel import SQLModel

HERE = pathlib.Path(__file__)
DATA_DIR = HERE.parents[1] / "data"
HOUSES_CSV = DATA_DIR / "houses.csv"


def from_csv(model: SQLModel, path: pathlib) -> List[SQLModel]:
    with open(path, mode="r") as csv_file:
        return [model.parse_obj(row) for row in csv.DictReader(csv_file)]
