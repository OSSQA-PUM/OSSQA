import json
import pytest
import os.path
from flask import Flask
from flask.testing import FlaskClient
from typing import Generator

from database.models import db, SBOM, Dependency, DependencyCheck
from database.server import create_test_app

CHECKS_PER_DEPENDENCY = 3  # This is based on what is in the test data files, not what is in actual analysis results 


@pytest.fixture(scope="module")
def app() -> Generator[Flask, None, None]:
    app = create_test_app()

    yield app
    
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="module")
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="module")
def sbom_results_list() -> list[dict]:
    # TODO: add more test data
    # TODO: replace test data based on actual analysis results
    #       (DONT FORGET TO UPDATE CHECKS_PER_DEPENDENCY WHEN YOU DO)
    data = []
    for i in range(1, 2):
        file_name = f"src/tests/add_sbom_{i}.json"
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                data.append(json.load(file))
    return data


def test_add_sbom(client, sbom_results_list):
    min_dependency_count = 0  # The amount of dependencies if maximum possible dependencies are shared between sboms
    max_dependency_count = 0  # The amount of dependencies if no dependencies are shared between sboms

    for sbom_results in sbom_results_list:
        min_dependency_count = max(Dependency.query.count(), len(sbom_results["components"]))
        max_dependency_count = Dependency.query.count() + len(sbom_results["components"])

        response = client.post("/add_SBOM", json=sbom_results)
        assert response.status_code == 201
    
    assert SBOM.query.count() == len(sbom_results_list)
    assert Dependency.query.count () >= min_dependency_count
    assert Dependency.query.count () <= max_dependency_count
    assert DependencyCheck.query.count() == Dependency.query.count() * CHECKS_PER_DEPENDENCY


def test_get_sbom(client, sbom_results_list):
    for i in range(1, len(sbom_results_list) + 1):
        # Tests getting each SBOM added by sbom_results_list
        response = client.get("/get_SBOM", json={"id": i})
        assert response.status_code == 200

    for i in range(len(sbom_results_list) + 1, len(sbom_results_list) + 10):
        # Tests getting SBOMs not added by sbom_results_list
        response = client.get("/get_SBOM", json={"id": i})
        assert response.status_code == 404


def test_get_existing_dependencies(client, sbom_results_list):
    existing_dependencies = []
    for sbom_results in sbom_results_list:
        for component in sbom_results["components"]:
            existing_dependencies.append({
                "name": component["name"],
                "version": component["version"],
            })
    non_existing_dependencies = [
        {
            "name": "nonexistingcomponent1",
            "version": "nonexistingversion1",
        },{
            "name": "nonexistingcomponent2",
            "version": "nonexistingversion2",
        },{
            "name": "nonexistingcomponent3",
            "version": "nonexistingversion3",
        }
    ]
    mixed_dependencies = existing_dependencies + non_existing_dependencies

    def check_existing_dependencies(response):
        for dependency in response.json:
            is_found = False
            for existing_dep in existing_dependencies:
                name_version = f"{existing_dep["name"]}@{existing_dep["version"]}"
                if dependency["name_version"] == name_version:
                    is_found = True
                    break
            assert is_found

    def check_non_existing_dependencies(response):
        for dependency in response.json:
            is_not_found = True
            for non_existing_dep in non_existing_dependencies:
                name_version = f"{non_existing_dep["name"]}@{non_existing_dep["version"]}"
                if dependency["name_version"] == name_version:
                    is_not_found = False
                    break
            assert is_not_found

    # Test where all dependencies exist
    response = client.get("/get_existing_dependencies", json=existing_dependencies)
    assert response.status_code == 200
    assert len(response.json) == len(existing_dependencies)
    check_existing_dependencies(response)
    check_non_existing_dependencies(response)

    # Test where some dependencies exist
    response = client.get("/get_existing_dependencies", json=mixed_dependencies)
    assert response.status_code == 200
    assert len(response.json) == len(existing_dependencies)
    check_existing_dependencies(response)
    check_non_existing_dependencies(response)

    # Test where no dependencies exist
    response = client.get("/get_existing_dependencies", json=non_existing_dependencies)
    assert response.status_code == 200
    assert len(response.json) == 0
    check_existing_dependencies(response)
    check_non_existing_dependencies(response)

    # Test where no dependencies are sent
    response = client.get("/get_existing_dependencies", json=[])
    assert response.status_code == 200
    assert len(response.json) == 0
    check_existing_dependencies(response)
    check_non_existing_dependencies(response)
