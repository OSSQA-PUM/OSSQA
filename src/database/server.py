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
    repo_commit = component["repo"]["name"] + component["repo"]["commit"]
    score = component["score"]
    dep = Dependency.query.filter_by(repo_commit=repo_commit).first()
    if dep is None:
        return Dependency(repo_commit=repo_commit, score=score)
    return dep


@app.route("/add_SBOM", methods=["POST"])
def add_SBOM():
    data = request.json
    try:
        serialNumber = data["serialNumber"]
    except KeyError:
        serialNumber = data["$schema"]
    version = data["version"]
    sbom = SBOM.query.filter_by(serialNumber=serialNumber).first()
    if sbom is not None:
        return "SBOM already exists", 409

    sbom = SBOM(serialNumber=serialNumber, version=version)
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
                    #print("updating check")
                    check.score = score
                    check.reason = reason
                    check.details = details
                    db.session.commit()
                else:  # if check does not exist, create it
                    #print("creating check: " + name + " for " + dep.repo_commit)
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


def initialize_db():
    app.app_context().push()
    db.drop_all()
    db.create_all()
