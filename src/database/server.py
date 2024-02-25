from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./our.db'
db = SQLAlchemy(app)

dependency_sbom = db.Table('dependency_sbom',
                           db.Column('dependency_id', db.Integer, db.ForeignKey('dependency.id'), primary_key=True),
                           db.Column('sbom_id', db.Integer, db.ForeignKey('sbom.id'), primary_key=True)
                           )


class Dependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        result = {'id': self.id, 'score': self.score}
        return result


class SBOM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    dependencies = db.relationship('Dependency', secondary=dependency_sbom, lazy='subquery',
                                   backref='sboms', cascade='all, delete')

    def to_dict(self):
        result = {'name': self.name, 'id': self.id}
        return result


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


# dependency cannot be null
@app.route("/add_dependency", methods=["POST"])
def add_dependency():
    data = request.json
    dep_id = data["id"]
    score = data["score"]
    dep = Dependency(id=dep_id, score=score)
    db.session.add(dep)
    db.session.commit()
    return jsonify({"id": dep_id, "score": score}), 201


@app.route("/add_SBOM", methods=["POST"])
def add_SBOM():
    data = request.json
    id = data["id"]
    name = data["name"]
    sbom = SBOM(id=id, name=name)
    db.session.add(sbom)
    db.session.commit()
    return jsonify({"id": id, "name": name}), 201


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
