from flask import Flask, jsonify, request

from database.models import db, dependency_sbom

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./our.db'
db.init_app(app)
from database.models import Dependency, DependencyCheck, SBOM


@app.errorhandler(404)
def page_not_found(e):
    return "Not found", 404


@app.errorhandler(405)
def method_not_allowed(e):
    return "Method not allowed", 405


@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return "generic error response", 500


def add_dependency_to_sbom(component):
    """
    Add a dependency to the sbom
    Args:
        component: component to turn into a dependency

    Returns:
        Dependency: dependency to be added
    """
    repo_commit = component["repo"]["name"] + component["repo"]["commit"]
    score = component["score"]
    dep = Dependency.query.filter_by(repo_commit=repo_commit).first()
    if dep is None:
        return Dependency(repo_commit=repo_commit, score=score)
    return dep


@app.route("/add_SBOM", methods=["POST"])
def add_SBOM():
    """
    Add a SBOM to the database
    Returns:
        json: the added SBOM
    """
    data = request.json
    try:
        serialNumber = data["serialNumber"]
    except KeyError:
        serialNumber = data["$schema"]

    sbom = SBOM(serialNumber=serialNumber,
                version=data["version"],
                repo_name=data["name"],
                repo_version=data["repo_version"])
    db.session.add(sbom)
    db.session.commit()
    # go through dependencies and add them to sbom
    for component in data["components"]:
        dep = add_dependency_to_sbom(component)
        if dep is not None:
            # check if dependency is new to db
            if dep not in sbom.dependencies:
                db.session.add(dep)
                db.session.commit()
                sbom.dependencies.append(dep)
                dep.sboms.append(sbom)
                db.session.commit()
            # update or add checks
            for check in component["checks"]:
                details = check["details"]
                if details is None:
                    details = ""
                if isinstance(details, list):
                    details = ". ".join(details)
                score = check["score"]
                reason = check["reason"]
                name = check["name"]

                # if check exists, update it
                check = DependencyCheck.query.filter_by(name=name, dependency_repo=dep.repo_commit).first()
                if check is not None:
                    check.score = score
                    check.reason = reason
                    check.details = details
                    db.session.commit()
                else:  # if check does not exist, create it
                    check = DependencyCheck(details=details, score=score, reason=reason, name=name,
                                            dependency_repo=dep.repo_commit)
                    db.session.add(check)
                    db.session.commit()

                # add check to dependency if it's not already there
                if check not in dep.checks:
                    dep.checks.append(check)
                    check.dependency_repo = dep
                    db.session.commit()

    return jsonify(sbom.to_dict()), 201


@app.route("/get_SBOM", methods=["GET"])
def get_SBOM():
    """
    Get a SBOM from the database
    Returns:
        json: the SBOM
    """
    data = request.json
    serial_number = data["serial_number"]
    sbom = db.get_or_404(SBOM, serial_number)
    return jsonify(sbom.to_dict()), 200


def initialize_db():
    """
    Initialize the database
    """
    app.app_context().push()
    db.drop_all()
    db.create_all()
