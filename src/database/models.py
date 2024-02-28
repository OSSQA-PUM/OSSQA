from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    details = db.Column(db.String(60), primary_key=True) # TODO: details can be null, change primary key
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