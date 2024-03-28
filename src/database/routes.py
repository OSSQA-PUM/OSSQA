"""
This module handles the endpoints that the backend communication interface
interfaces with. It also handles functionality for creating and updating
various objects in the database.
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from .models import SBOM, Dependency, DependencyCheck


def create_or_update_dependency(component: dict) -> tuple[Dependency, bool]:
    """
    Create or update a dependency in the database.

    Args:
        component (dict): The data of the dependency to be added.

    Returns:
        tuple[Dependency, bool]: The created/updated dependency and a boolean
            indicating if it was created or not.
    """
    name_version = f"{component['name']}@{component['version']}"
    score = component["score"]

    dependency = Dependency.query.filter_by(name_version=name_version).first()
    if dependency:
        dependency.score = score
        return dependency, False
    else:
        return Dependency(name_version=name_version, score=score), True


def create_or_update_check(data: dict, dep_name_verison: str) \
    -> tuple[DependencyCheck, bool]:
    """
    Create or update a check in the database

    Args:
        data (dict): The data of the check to be added.
        dep_name_verison (str): The dependency name and version to connect the
            check with.

    Returns:
        tuple[DependencyCheck, bool]: The check and a boolean indicating if it
            was created or not.
    """
    name = data["name"]
    details = data["details"]
    reason = data["reason"]
    score = data["score"]

    check = DependencyCheck.query.filter_by(
        name=name,
        dep_name_version=dep_name_verison,
    ).first()

    if check:
        check.score = score
        check.reason = reason
        check.details = details
        return check, False
    else:
        check = DependencyCheck(name=name,
                                dep_name_version=dep_name_verison,
                                details=details,
                                reason=reason,
                                score=score)
        return check, True


def register_endpoints(app: Flask, db: SQLAlchemy):
    """
    Registers all endpoints with a flask app and its database.

    Args:
        app (Flask): The flask app.
        db (SQLAlchemy): The database.
    """
    @app.errorhandler(404)
    def page_not_found(error):
        print("Error:", error)
        return "Not found", 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        print("Error:", error)
        return "Method not allowed", 405

    @app.errorhandler(Exception)
    def handle_exception(error):
        print("Error:", error)
        return "Internal server error", 500

    @app.route("/add_SBOM", methods=["POST"])
    def add_sbom():
        """
        Adds an SBOM to the database.

        Args:
            json (object): The SBOM and its score, along with its dependencies
                and their scores.

        Returns:
            json (object): The added SBOM.
        """
        # NOTE: should we really commit before the absolute end?
        #       what if something fails?

        sbom = SBOM(serial_number=request.json["serialNumber"],
                    version=request.json["version"],
                    repo_name=request.json["name"],
                    repo_version=request.json["repo_version"])
        db.session.add(sbom)
        db.session.commit()

        for component in request.json["components"]:
            dependency, new_dependency = create_or_update_dependency(component)
            if new_dependency:
                db.session.add(dependency)
            sbom.dependencies.append(dependency)
            db.session.commit()

            for check_data in component["checks"]:
                check, new_check = create_or_update_check(
                    check_data,
                    dependency.name_version,
                )
                if new_check:
                    db.session.add(check)
                    dependency.checks.append(check)
                db.session.commit()

        return jsonify(sbom.to_dict()), 201

    @app.route("/get_SBOM", methods=["GET"])
    def get_sbom():
        """
        Get an SBOM from the database.

        Args:
            json (object): Object containing the SBOM primary key.

        Returns:
            json (object): The SBOM.
        """
        sbom_id = request.json["id"]  # TODO: get as url parameter instead
        sbom = db.get_or_404(SBOM, sbom_id)
        return jsonify(sbom.to_dict()), 200

    @app.route("/get_existing_dependencies", methods=["GET"])
    def get_existing_dependencies():
        """
        Get existing dependencies in the database, based on which are sent in.

        Args:
            json (array): An array of objects containing the name and version
                of each dependency that is to be checked if it exists.

        Returns:
            json (array): The existing dependencies.
        """
        dep_name_versions: list[str] = []
        for dep in request.json:
            dep_name_versions.append(f"{dep['name']}@{dep['version']}")

        dependencies = []
        for dep_name_version in dep_name_versions:
            dependency = Dependency.query.filter_by(
                name_version=dep_name_version
            ).first()
            if not dependency:
                continue
            dependencies.append(dependency.to_dict())

        return jsonify(dependencies), 200