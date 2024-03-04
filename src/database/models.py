from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint

db = SQLAlchemy()

dependency_sbom = db.Table('dependency_sbom',
                           db.Column('dependency_name', db.String(60), db.ForeignKey('dependency.name'),
                                     primary_key=True),
                           db.Column('dependency_version', db.String(60), db.ForeignKey('dependency.version'),
                                     primary_key=True),
                           db.Column('sbom_id', db.Integer, db.ForeignKey('sbom.id'),
                                     primary_key=True)
                           )


class Dependency(db.Model):
    name = db.Column(db.String(60), primary_key=True)
    version = db.Column(db.String(60), primary_key=True)
    score = db.Column(db.Integer, unique=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    sboms = db.relationship('SBOM', secondary=dependency_sbom, lazy='subquery',
                            back_populates='dependencies')
    checks = db.relationship('DependencyCheck', backref='dependency', lazy=True)

    def to_dict(self):
        return {'name': self.name,
                'version': self.version,
                'score': self.score,
                'date_added': self.date_added,
                'checks': [check.to_dict() for check in self.checks],
                }


class DependencyCheck(db.Model):
    details = db.Column(db.String(60), unique=False)  # TODO: details can be null, change primary key
    score = db.Column(db.Double, unique=False)
    reason = db.Column(db.String(60), unique=False)
    name = db.Column(db.String(60), unique=False, primary_key=True)
    dependency_repo = db.Column(db.String(60), db.ForeignKey('dependency.repo_commit'), unique=False, primary_key=True)

    def to_dict(self):
        return {'details': self.details,
                'score': self.score,
                'reason': self.reason,
                'name': self.name,
                }


class SBOM(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    serialNumber = db.Column(db.String(60), unique=False)
    version = db.Column(db.String(60), unique=False)
    repo_name = db.Column(db.String(60), unique=False)
    repo_version = db.Column(db.String(60), unique=False)

    dependencies = db.relationship('Dependency', secondary=dependency_sbom, lazy='subquery', back_populates='sboms')

    def to_dict(self):
        return {'serialNumber': self.serialNumber,
                'version': self.version,
                'id': self.id,
                'repo_name': self.repo_name,
                'repo_version': self.repo_version,
                'dependencies': [dep.to_dict() for dep in self.dependencies],
                }
