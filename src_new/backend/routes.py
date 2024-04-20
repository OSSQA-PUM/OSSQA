"""
This module handles the endpoints that the backend communication interface
interfaces with. It also handles functionality for creating and updating
various objects in the database.
"""
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from models import SBOM, Dependency


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
        return "NOT IMPLEMENTED YET", 501 # TODO implement

    @app.route("/sbom", methods=["GET"])
    def get_sbom_names():
        """
        Gets the name of every SBOM in the database.

        Returns:
            json (array): The list of SBOM names.
        """
        names = set()
        for sbom in SBOM.query.all():
            names.add(sbom.name)
        return jsonify(list(names)), 200


    @app.route("/sbom/<name>", methods=["GET"])
    def get_sboms_by_name(name: str):
        """
        Gets a list of SBOMs with a specific name.

        Args:
            name (str): The name to query the database with.

        Returns:
            json (array): The list of SBOMs.
        """
        sboms = SBOM.query.filter_by(name=name).all()
        sbom_dicts = [sbom.to_dict() for sbom in sboms]
        return jsonify(sbom_dicts), 200

    @app.route("dependency/existing", methods=["GET"])
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
        dependencies = []
        for name, version in request.json:
            dependency = Dependency.query.filter_by(name=name, version=version).first()
            if dependency:
                dependencies.append(dependency.to_dict())
        return jsonify(dependencies), 200
