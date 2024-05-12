"""
This module contains tests for each route in the flask app.
"""
import json
from typing import Generator

from flask.testing import FlaskClient
from pytest import fixture, FixtureRequest

from backend.server import create_test_app
from backend.models import db
from tests.backend.sboms import PATHS


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
    resp = client.post("/sbom", json=sbom)
    assert resp.status_code == 201
    # TODO: make sure the right objects exist in the database


def test_update_sbom(client: FlaskClient, sbom: dict):
    resp = client.post("/sbom", json=sbom)
    assert resp.status_code == 201
    # TODO: make sure the right objects exist in the database


def test_sbom_names(client: FlaskClient, sbom: dict):
    resp = client.get("/sbom")
    assert resp.status_code == 200

    found_name = False
    for name in resp.json:
        if name == sbom["repo_name"]:
            found_name = True
            break
    assert found_name


def test_get_sboms_by_name(client: FlaskClient, sbom: dict):
    resp = client.get(f"/sbom/{sbom["repo_name"]}")
    assert resp.status_code == 200

    for resp_sbom in resp.json:
        assert resp_sbom["serialNumber"] == sbom["serialNumber"]
        assert resp_sbom["version"] == sbom["version"]
        assert resp_sbom["metadata"]["component"]["name"] == sbom["repo_name"]
        assert resp_sbom["metadata"]["component"]["version"] == sbom["repo_version"]
        for component in resp_sbom["components"]:
            found_component = False
            for dependency in sbom["scored_dependencies"]:
                found_component = component["name"] == dependency["name"] and \
                    component["version"] == dependency["version"]
                if found_component:
                    break
            assert found_component


def test_get_existing_dependencies(client: FlaskClient, sbom: dict):
    dep_name_versions = []
    for dep in sbom["scored_dependencies"]:
        dep_name_versions.append([dep["platform_path"], dep["name"], dep["version"]])

    resp = client.get("/dependency/existing", json=dep_name_versions)
    assert resp.status_code == 200

    for component in resp.json:
        print(component)
        assert [component["platformPath"], component["name"], component["version"]] in dep_name_versions
