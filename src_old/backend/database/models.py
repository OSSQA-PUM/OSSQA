"""
This module handles the configuration of each model that is in the database.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

dependency_sbom = db.Table("dependency_sbom",
                           db.Column("dep_name_version", db.String(120),
                                     db.ForeignKey("dependency.name_version"),
                                     primary_key=True),
                           db.Column("sbom_id", db.Integer,
                                     db.ForeignKey("sbom.id"),
                                     primary_key=True))


class DependencyCheck(db.Model):
    """
    A OpenSSF Scorecard check associated with a dependency.
    """
    name = db.Column(db.String(60), unique=False, primary_key=True)
    dep_name_version = db.Column(db.String(120),
                                 db.ForeignKey("dependency.name_version"),
                                 unique=False,
                                 primary_key=True)

    details = db.Column(db.String(60), unique=False)
    score = db.Column(db.Double, unique=False)
    reason = db.Column(db.String(60), unique=False)

    def to_dict(self) -> dict:
        return {"name": self.name,
                "details": self.details,
                "score": self.score,
                "reason": self.reason}


class Dependency(db.Model):
    """
    A dependency, with an OpenSSF Scorecard score, associated with SBOMs.
    """
    name_version = db.Column(db.String(120), primary_key=True)

    score = db.Column(db.Double, unique=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    url = db.Column(db.String(120), unique=False)

    checks = db.relationship("DependencyCheck",
                             backref="dependency",
                             lazy=True)
    sboms = db.relationship("SBOM",
                            secondary=dependency_sbom,
                            lazy="subquery",
                            back_populates="dependencies")

    def to_dict(self) -> dict:
        return {"name_version": self.name_version,
                "score": self.score,
                "date_added": self.date_added,
                "checks": [check.to_dict() for check in self.checks]}


class SBOM(db.Model):
    """
    An SBOM associated with dependencies.
    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    serial_number = db.Column(db.String(60), unique=False)
    version = db.Column(db.String(60), unique=False)
    repo_name = db.Column(db.String(60), unique=False)
    repo_version = db.Column(db.String(60), unique=False)

    dependencies = db.relationship("Dependency",
                                   secondary=dependency_sbom,
                                   lazy="subquery",
                                   back_populates="sboms")

    def to_dict(self) -> dict:
        dependencies = [dep.to_dict() for dep in self.dependencies]
        return {"serialNumber": self.serial_number,
                "version": self.version,
                "repo_name": self.repo_name,
                "repo_version": self.repo_version,
                "dependencies": dependencies}
