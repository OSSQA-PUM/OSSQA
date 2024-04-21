"""
This module handles the configuration of each model that is in the database.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

dependency_sbom = db.Table("dependency_sbom",
                           db.Column("dependency_id", db.Integer,
                                     db.ForeignKey("dependency.id"),
                                     primary_key=True),
                           db.Column("sbom_id", db.Integer,
                                     db.ForeignKey("sbom.id"),
                                     primary_key=True))


class Check(db.Model):
    """
    A model representing a OpenSSF Scorecard Chec.
    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), unique=False)
    score = db.Column(db.Integer, unique=False)
    reason = db.Column(db.String(255), unique=False)
    # TODO details

    scorecard_id = db.Column(db.Integer, db.ForeignKey("scorecard.id"),
                             nullable=False)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "score": self.name,
            "reason": self.reason,
            # TODO details,
        }



class Scorecard(db.Model):
    """
    A model representing a OpenSSF Scorecard.
    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.String(10), unique=False)
    aggregate_score = db.Column(db.Double, unique=False)

    checks = db.relationship("Check", backref="scorecard", lazy=True)
    dependency_id = db.Column(db.Integer, db.ForeignKey("dependency.id"),
                              nullable=False)

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "score": self.aggregate_score,
            "checks": [check.to_dict() for check in self.checks],
        }


class Dependency(db.Model):
    """
    A dependency with a score from OpenSSF Scorecard.
    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), unique=False)
    version = db.Column(db.String(255), unique=False)

    scorecard = db.relationship("Scorecard", backref="dependency", lazy=True,
                                uselist=False)
    sboms = db.relationship("SBOM", secondary=dependency_sbom, lazy="subquery",
                            back_populates="dependencies")

    def to_dict(self) -> dict:
        """
        Represent the dependency as a dict resembling its original json format.

        Returns
            dict: The dict representing the dependency.
        """
        return {
            "name": self.name,
            "version": self.version,
            "scorecard": self.scorecard.to_dict(),
        }


class SBOM(db.Model):
    """
    A software bill of materials (SBOM).
    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    serial_number = db.Column(db.String(60), unique=False)
    version = db.Column(db.String(255), unique=False)
    repo_name = db.Column(db.String(255), unique=False)
    repo_version = db.Column(db.String(255), unique=False)

    dependencies = db.relationship("Dependency", secondary=dependency_sbom,
                                   lazy="subquery", back_populates="sboms")

    def to_dict(self) -> dict:
        """
        Represent the SBOM as a dict resembling its original json format.

        Returns
            dict: The dict representing the SBOM.
        """
        return {
            "serialNumber": self.serial_number,
            "version": self.version,
            "metadata": {
                "component": {
                    "name": self.repo_name,
                    "version": self.repo_version,
                },
            },
            "components": [c.to_dict() for c in self.dependencies],
        }
