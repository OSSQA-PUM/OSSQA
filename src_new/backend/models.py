from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


"""
---------------------------------------
Anteckningar:
---------------------------------------
Ett existernade SBOM-objekt ska uppdateras när
- version
- repo_name
- repo_version
är samma som det som skickas in till "POST /sbom".

För att ingen ändring har skett i SBOM:en (version är samma)
och ingen ändring har skett i repot (repo_version är samma).

Om ett repo ändras utan att repo_version ändras bör SBOM version.

Annars ska ett nytt SBOM-objekt skapas.
---------------------------------------
"""

class SBOM(db.Model):
    """
    A software bill of materials (SBOM).
    """
    serial_number = db.Column(db.String(60), unique=False)
    version = db.Column(db.String(255), unique=False)
    
    def to_dict(self) -> dict:
        return {
            "serialNumber": self.serial_number,
            "version": self.version,
        }
