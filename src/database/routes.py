from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from .models import SBOM, Dependency, DependencyCheck


def create_or_update_dependency(component: dict) -> tuple[Dependency, bool]:
    """
    Create or update a dependency in the database
    Args:
        component: the data of the dependency to be added

    Returns:
        tuple[Dependency, bool]: the created/updated dependency and a boolean indicating if it was created or not
    """
    name_version = f"{component['name']}@{component['version']}"
    score = component["score"]
    
    if dependency := Dependency.query.filter_by(name_version=name_version).first():
        dependency.score = score
        return dependency, False
    else:
        return Dependency(name_version=name_version, score=score), True


def create_or_update_check(data: dict, dep_name_verison: str) -> tuple[DependencyCheck, bool]:
    """
    Create or update a check in the database
    Args:
        data: the data of the check to be added
        dep_name_verison: the dependency name and version to connect the check with

    Returns:
        tuple[DependencyCheck, bool]: the created/updated check and a boolean indicating if it was created or not
    """
    name = data["name"]
    details = data["details"]
    reason = data["reason"]
    score = data["score"]

    if check := DependencyCheck.query.filter_by(name=name, dependency_name_version=dep_name_verison).first():
        check.score = score
        check.reason = reason
        check.details = details
        return check, False
    else:
        return DependencyCheck(name=name,
                               dependency_name_version=dep_name_verison,
                               details=details,
                               reason=reason,
                               score=score), True
    


def register_endpoints(app: Flask, db: SQLAlchemy):
    @app.errorhandler(404)
    def page_not_found(error):
        return "Not found", 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return "Method not allowed", 405

    @app.errorhandler(Exception)
    def handle_exception(error):
        print("Error:", error)
        return "Internal server error", 500
    
    @app.route("/add_SBOM", methods=["POST"])
    def add_sbom():
        """
        Add a SBOM to the database
        Returns:
            json: the added SBOM
        """
        # NOTE: should we really commit before the absolute end?
        #       what if something fails?

        sbom = SBOM(serial_number=request.json["serialNumber"],
                    version=request.json["version"],
                    repo_name=request.json["name"],
                    repo_version=request.json["repo_version"])
        db.session.add(sbom)
        db.session.commit()
        print("Created sbom")
        
        for component in request.json["components"]:
            dependency, new_dependency = create_or_update_dependency(component)
            if new_dependency:
                db.session.add(dependency)
            sbom.dependencies.append(dependency)
            db.session.commit()
            print("Created/updated dep")

            for check_data in component["checks"]:
                check, new_check = create_or_update_check(check_data, dependency.name_version)
                if new_check:
                    db.session.add(check)
                    dependency.checks.append(check)
                db.session.commit()
            print("Created/updated checks")

        return jsonify(sbom.to_dict()), 201

    @app.route("/get_SBOM", methods=["GET"])
    def get_sbom():
        """
        Get a SBOM from the database
        Returns:
            json: the SBOM
        """
        sbom_id = request.json["id"] # TODO: get as url parameter instead
        sbom = db.get_or_404(SBOM, sbom_id)
        return jsonify(sbom.to_dict()), 200
    
    @app.route("/get_existing_dependencies", methods=["GET"])
    def get_existing_dependencies():
        """
        Get existing dependencies from the database
        Returns:
            json: a list of dependencies
        """
        dep_name_versions = [f"{dep['name']}@{dep['version']}" for dep in request.json]

        dependencies = []
        for dep_name_version in dep_name_versions:
            dependency = Dependency.query.filter_by(name_version=dep_name_version).first()
            if dependency is None:
                continue
            dependencies.append(dependency.to_dict())

        return jsonify(dependencies), 200