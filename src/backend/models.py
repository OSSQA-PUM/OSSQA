"""
This module handles the configuration of each database model and their
relations.
"""
import json
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
    A model representing a OpenSSF Scorecard Check.
    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), unique=False)
    score = db.Column(db.Integer, unique=False)
    reason = db.Column(db.String(255), unique=False)
    details = db.Column(db.Text, unique=False)

    scorecard_id = db.Column(db.Integer, db.ForeignKey("scorecard.id"),
                             nullable=False)

    def to_dict(self) -> dict:
        """
        Creates a dictionary representing the check, that can be used in
        responses.

        Returns
            dict: A dictionary representation of the check.
        """
        return {
            "name": self.name,
            "score": self.score,
            "reason": self.reason,
            "details": self.details
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
        """
        Creates a dictionary representing the scorecard, that can be used in
        responses.

        Returns
            dict: A dictionary representation of the scorecard.
        """
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
    platform_path = db.Column(db.String(255), unique=False)
    component = db.Column(db.Text, unique=False)

    scorecard = db.relationship("Scorecard", backref="dependency", lazy=True,
                                uselist=False)
    sboms = db.relationship("SBOM", secondary=dependency_sbom, lazy="subquery",
                            back_populates="dependencies")

    def to_dict(self) -> dict:
        """
        Creates a dictionary representing the dependency, that can be used in
        responses.

        Returns
            dict: A dictionary representation of the dependency.
        """
        res = {}
        for key, value in json.loads(self.component).items():
            res[key] = value
        res["scorecard"] = self.scorecard.to_dict()
        return res


class SBOM(db.Model):
    """
    A software bill of materials (SBOM).
    """
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    serial_number = db.Column(db.String(60), unique=False)
    version = db.Column(db.Integer, unique=False)
    repo_name = db.Column(db.String(255), unique=False)
    repo_version = db.Column(db.String(255), unique=False)

    dependencies = db.relationship("Dependency", secondary=dependency_sbom,
                                   lazy="subquery", back_populates="sboms")

    def to_dict(self) -> dict:
        """
        Creates a dictionary representing the SBOM, that can be used in
        responses.

        Returns
            dict: A dictionary representation of the SBOM.
        """
        return {
            "bomFormat": "CycloneDX",
            "specVersion": "1.2",
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
