"""
This module handles the endpoints that the backend communication interface
interfaces with. It also handles functionality for creating and updating
various objects in the database.
"""
import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from backend.models import SBOM, Dependency, Scorecard, Check


def register_endpoints(app: Flask, db: SQLAlchemy):
    """
    Registers all endpoints with a flask app and its database.

    Args:
        app (Flask): The flask app.
        db (SQLAlchemy): The database.
    """

    @app.route("/sbom", methods=["POST"])
    def add_sbom():
        """
        Adds an SBOM to the database.

        Args:
            json (object): A JSON object containing the SBOM data.

        Status codes:
            400: If the request is not of type JSON.
            201: If the SBOM could be added to the database.
        """
        if not request.is_json:
            return "", 400
        sbom_json = request.json

        sbom: SBOM = SBOM.query.filter_by(
            version=sbom_json["version"],
            repo_name=sbom_json["repo_name"],
            repo_version=sbom_json["repo_version"],
        ).first()

        if not sbom:
            sbom = SBOM(
                serial_number=sbom_json["serialNumber"],
                version=sbom_json["version"],
                repo_name=sbom_json["repo_name"],
                repo_version=sbom_json["repo_version"],
            )
            db.session.add(sbom)

        for dep_json in sbom_json["scored_dependencies"]:
            dep: Dependency = Dependency.query.filter_by(
                platform_path=dep_json["platform_path"],
                name=dep_json["name"],
                version=dep_json["version"],
            ).first()
            # Get the attributes that are not part of the dependency scorecard
            dep_component = {}
            for k, v in dep_json.items():
                if k not in (
                        "platform_path",
                        "scorecard",
                        "failure_reason",
                        "reach_requirement"):
                    dep_component[k] = v

            scorecard_json = dep_json["scorecard"]

            if dep:
                scorecard: Scorecard = dep.scorecard
                for check in scorecard.checks:
                    db.session.delete(check)
                db.session.delete(scorecard)
            else:
                dep = Dependency(
                    platform_path=dep_json["platform_path"],
                    name=dep_json["name"],
                    version=dep_json["version"],
                    component=json.dumps(dep_component),
                )
                sbom.dependencies.append(dep)
                db.session.add(dep)

            scorecard = Scorecard(
                date=scorecard_json["date"],
                aggregate_score=scorecard_json["score"],
            )
            dep.scorecard = scorecard
            db.session.add(scorecard)

            for check_json in scorecard_json["checks"]:
                check = Check(
                    name=check_json["name"],
                    score=check_json["score"],
                    reason=check_json["reason"],
                )
                scorecard.checks.append(check)
                db.session.add(check)

        db.session.commit()
        return "", 201

    @app.route("/sbom", methods=["GET"])
    def get_sbom_names():
        """
        Fetches the name of every SBOM in the database.

        Returns:
            json (array): The list of SBOM names.

        Status codes:
            200: If the list of SBOM names could be created.
        """
        names = set()
        for sbom in SBOM.query.all():
            names.add(sbom.repo_name)
        return jsonify(list(names)), 200

    @app.route("/sbom/<path:repo_name>", methods=["GET"])
    def get_sboms_by_name(repo_name: str):
        """
        Fetches a list of SBOMs with a specific name.

        Args:
            repo_name (str): The name to query the database with.

        Returns:
            json (array): The list of SBOMs.

        Status codes:
            200: If the list of SBOMs could be created.
        """
        sboms = SBOM.query.filter_by(repo_name=repo_name).all()
        sbom_dicts = [sbom.to_dict() for sbom in sboms]
        return jsonify(sbom_dicts), 200

    @app.route("/dependency/existing", methods=["GET"])
    def get_existing_dependencies():
        """
        Fetches all dependencies that have an existing match in
        the database.

        Args:
            json (array): The list of dependency dictionaries, containing
                containing the name, version, and platform_path.

        Returns:
            json (array): The list of dependecies.

        Status codes:
            400: If the request is not of type JSON.
            200: If the list of dependencies could be created.
        """
        if not request.is_json:
            return jsonify([]), 400

        dependencies = []
        for dep in request.json:
            version = dep["version"]
            name = dep["name"]
            try:
                path = dep["platform_path"]
            except KeyError:
                continue
            dependency = Dependency.query.filter_by(
                platform_path=path, version=version, name=name).first()
            if dependency:
                dependencies.append(dependency.to_dict())
        return jsonify(dependencies), 200


def register_test_endpoints(app: Flask, db: SQLAlchemy):
    """
    Registers all test endpoints with a flask app and its database.

    Args:
        app (Flask): A flask app.
        db (SQLAlchemy): A database.
    """

    @app.route("/test/reset", methods=["POST"])
    def reset_database():
        """
        Drops and recreates the database.

        Status codes:
            200: If the datebase could be dropped and recreated.
        """
        db.drop_all()
        db.create_all()
        return "", 200
