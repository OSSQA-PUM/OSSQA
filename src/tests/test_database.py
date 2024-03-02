import json
import pytest
import os.path
from flask import Flask
from flask.testing import FlaskClient
from typing import Generator

from database.models import SBOM, Dependency, DependencyCheck


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    from database.server import app, db
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///./test.db",
    })
    app.app_context().push()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def sbom_results() -> list[dict]:
    sbom_results = []
    for i in range(1, 10):
        file_name = f"src/tests/SBOM{i}_results.json"
        if os.path.exists(file_name):
            file = open(file_name, "r")
            result = json.load(file)
            file.close()
            sbom_results.append(result)
    return sbom_results


def test_add_sbom(client, sbom_results):
    results_posted = 0
    #min_dependencies = 0
    #max_dependencies = 0
    CHECKS_PER_DEPENDENCY = 18

    # TODO: There are duplicates in sbom_result["components"] so you can't reliably control the
    #       number of dependencies, uncomment dependency lines when this is fixed OR find another
    #       reliable way of controling it
    for sbom_result in sbom_results:
        results_posted += 1
        #min_dependencies = max(Dependency.query.count(), len(sbom_result["components"]))
        #max_dependencies = Dependency.query.count() + len(sbom_result["components"])

        response = client.post("/add_SBOM", json=sbom_result)
        assert response.status_code == 201

    assert SBOM.query.count() == results_posted
    #assert Dependency.query.count() >= min_dependencies
    #assert Dependency.query.count() <= max_dependencies
    assert Dependency.query.count() != 0  # TODO: remove when the two lines above can be tested reliably
    assert DependencyCheck.query.count() == CHECKS_PER_DEPENDENCY * Dependency.query.count()


def test_fetch_sbom(client, sbom_results):
    for sbom_result in sbom_results:
        serial_number = sbom_result.get("serialNumber", sbom_result.get("$schema"))

        response = client.get("/fetch_SBOM", json={"serial_number": serial_number})
        assert response.status_code == 200
        assert response.data["serialNumber"] == serial_number