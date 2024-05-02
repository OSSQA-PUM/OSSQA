"""
This module handles the endpoints that the backend communication interface
interfaces with. It also handles functionality for creating and updating
various objects in the database.
"""
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

    # TODO add proper error-handling methods

    @app.route("/sbom", methods=["POST"])
    def add_sbom():
        """
        Adds an SBOM to the database.

        Args:
             json (object): Object containing the SBOM data.
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
                name=dep_json["name"],
                version=dep_json["version"],
            ).first()
            scorecard_json = dep_json["dependency_score"]

            if dep:
                scorecard: Scorecard = dep.scorecard
                for check in scorecard.checks:
                    db.session.delete(check)
                db.session.delete(scorecard)
            else:
                dep = Dependency(
                    name=dep_json["name"],
                    version=dep_json["version"],
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
        Gets the name of every SBOM in the database.

        Returns:
            json (array): The list of SBOM names.
        """
        names = set()
        for sbom in SBOM.query.all():
            names.add(sbom.repo_name)
        return jsonify(list(names)), 200


    @app.route("/sbom/<path:repo_name>", methods=["GET"])
    def get_sboms_by_name(repo_name: str):
        """
        Gets a list of SBOMs with a specific name.

        Args:
            name (str): The name to query the database with.

        Returns:
            json (array): The list of SBOMs.
        """
        sboms = SBOM.query.filter_by(repo_name=repo_name).all()
        sbom_dicts = [sbom.to_dict() for sbom in sboms]
        return jsonify(sbom_dicts), 200

    @app.route("/dependency/existing", methods=["GET"])
    def get_existing_dependencies():
        """
        Gets a list of dependencies, based on the specified primary
        keys.

        Args:
            json (array): A list containing tuples with the name and version
                of each dependency.

        Returns:
            json (array): The list of dependecies.
        """
        if not request.is_json:
            return jsonify([]), 400

        dependencies = []
        for key in request.json:
            dependency = Dependency.query.filter_by(name=key, version=request.json[key]).first()
            if dependency:
                dependencies.append(dependency.to_dict())
        return jsonify(dependencies), 200


def register_test_endpoints(app: Flask, db: SQLAlchemy):
    """
    Registers all test endpoints with a flask app and its database.

    Args:
        app (Flask): The flask app.
        db (SQLAlchemy): The database.
    """

    @app.route("/test/reset", methods=["POST"])
    def reset_database():
        db.drop_all()
        db.create_all()
        return "", 200
