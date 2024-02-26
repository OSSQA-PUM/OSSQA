from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./our.db'
db = SQLAlchemy(app)

dependency_sbom = db.Table('dependency_sbom',
                           db.Column('dependency_purl', db.Integer, db.ForeignKey('dependency.purl'), primary_key=True),
                           db.Column('sbom_serialNumber', db.Integer, db.ForeignKey('sbom.serialNumber'),
                                     primary_key=True)
                           )


class Dependency(db.Model):
    purl = db.Column(db.String(60), primary_key=True)
    score = db.Column(db.Integer, unique=False)
    name = db.Column(db.String(60), unique=False)
    version = db.Column(db.String(60), unique=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    sboms = db.relationship('SBOM', secondary=dependency_sbom, lazy='subquery',
                            back_populates='dependencies')

    def to_dict(self):
        return {'purl': self.purl,
                'score': self.score,
                'name': self.name,
                'version': self.version,
                'date_added': self.date_added,
                }


class SBOM(db.Model):
    serialNumber = db.Column(db.String(60), primary_key=True)
    bomFormat = db.Column(db.String(60), unique=False)
    specVersion = db.Column(db.String(60), unique=False)
    version = db.Column(db.String(60), unique=False)

    dependencies = db.relationship('Dependency', secondary=dependency_sbom, lazy='subquery', back_populates='sboms')

    def to_dict(self):
        return {'serialNumber': self.serialNumber,
                'bomFormat': self.bomFormat,
                'specVersion': self.specVersion,
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


@app.route("/add_dependency", methods=["POST"])
def add_dependency():
    data = request.json
    dep_id = data["id"]
    score = data["score"]
    dep = Dependency(id=dep_id, score=score)
    db.session.add(dep)
    db.session.commit()
    return jsonify({"id": dep_id, "score": score}), 201


def add_dependency_to_sbom(component):
    name = component["name"]
    version = component["version"]
    purl = component["purl"]
    score = None
    dep = Dependency.query.filter_by(purl=purl).first()
    if dep is None:
        return Dependency(name=name, version=version, purl=purl, score=score)
    return dep


@app.route("/add_SBOM", methods=["POST"])
def add_SBOM():
    data = request.json
    bomFormat = data["bomFormat"]
    specVersion = data["specVersion"]
    try:
        serialNumber = data["serialNumber"]
    except KeyError:
        serialNumber = data["$schema"]
    version = data["version"]
    sbom = SBOM.query.filter_by(serialNumber=serialNumber).first()
    if sbom is not None:
        return "SBOM already exists", 409

    sbom = SBOM(bomFormat=bomFormat, specVersion=specVersion, serialNumber=serialNumber, version=version)
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


@app.route("/show/SBOM", methods=["GET"])
def get_message():
    data = request.json
    sbom_id = data["id"]
    sbom = SBOM.query.filter_by(id=sbom_id).first()
    if sbom is None:
        return "Not found", 404
    return jsonify(sbom.to_dict()), 200


def initialize_db():
    app.app_context().push()
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    app.debug = True
    app.run(port=5080)
