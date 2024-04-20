"""
This module contains tests for each route in the flask app.
"""
import json
from typing import Generator

from flask.testing import FlaskClient
from pytest import fixture, FixtureRequest

from server import create_test_app
from models import db
from tests.sboms import PATHS


@fixture(name="client", scope="module")
def client_fixture() -> Generator[FlaskClient, None, None]:
    """
    Creates a test client that handles requests to the test app.
    """
    app = create_test_app()
    yield app.test_client()
    db.session.remove()
    db.drop_all()


@fixture(name="sbom", params=PATHS, scope="module")
def sbom_fixture(request: FixtureRequest) -> dict:
    """
    Opens and reads the content of SBOMs.
    """
    with open(request.param, "r", encoding="utf-8") as sbom_file:
        return json.load(sbom_file)


def test_add_sbom(client: FlaskClient, sbom: dict):
    pass


def test_sbom_names(client: FlaskClient, sbom: dict):
    pass


def test_get_sboms_by_name(client: FlaskClient, sbom: dict):
    pass


def test_get_existing_dependencies(client: FlaskClient, sbom: dict):
    pass
