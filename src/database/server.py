from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./our.db'
db = SQLAlchemy(app)

dependency_sbom = db.Table('dependency_sbom',
                           db.Column('dependency_repo_commit', db.Integer, db.ForeignKey('dependency.repo_commit'),
                                     primary_key=True),
                           db.Column('sbom_serialNumber', db.Integer, db.ForeignKey('sbom.serialNumber'),
                                     primary_key=True)
                           )


class Dependency(db.Model):
    repo_commit = db.Column(db.String(60), primary_key=True)
    score = db.Column(db.Integer, unique=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    sboms = db.relationship('SBOM', secondary=dependency_sbom, lazy='subquery',
                            back_populates='dependencies')
    checks = db.relationship('DependencyCheck', backref='dependency', lazy=True)

    def to_dict(self):
        return {'repo_commit': self.repo_commit,
                'score': self.score,
                'name': self.name,
                'version': self.version,
                'date_added': self.date_added,
                }


class DependencyCheck(db.Model):
    details = db.Column(db.String(60), primary_key=True)
    score = db.Column(db.Double, unique=False)
    reason = db.Column(db.String(60), unique=False)
    name = db.Column(db.String(60), unique=False)
    dependency_repo = db.Column(db.String(60), db.ForeignKey('dependency.repo_commit'), unique=False)


    def to_dict(self):
        return {'details': self.details,
                'score': self.score,
                'reason': self.reason,
                'name': self.name,
                }


class SBOM(db.Model):
    serialNumber = db.Column(db.String(60), primary_key=True)
    version = db.Column(db.String(60), unique=False)

    dependencies = db.relationship('Dependency', secondary=dependency_sbom, lazy='subquery', back_populates='sboms')

    def to_dict(self):
        return {'serialNumber': self.serialNumber,
                'version': self.version,
                }


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
    for check in data["checks"]:
        details = check["details"]
        score = check["score"]
        reason = check["reason"]
        name = check["name"]
        check = DependencyCheck(details=details, score=score, reason=reason, name=name)
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

    for component in data["components"]:
        dep = add_dependency_to_sbom(component)
        if dep is not None:
            db.session.add(dep)
            db.session.commit()
            sbom.dependencies.append(dep)
            dep.sboms.append(sbom)
            db.session.commit()

    return jsonify(sbom.to_dict()), 201


def initialize_db():
    app.app_context().push()
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    app.debug = True
    app.run(port=5080)
