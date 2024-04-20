from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def register_endpoints(app: Flask, db: SQLAlchemy):
    """
    Registers all endpoints with a flask app and its database.

    Args:
        app (Flask): The flask app.
        db (SQLAlchemy): The database.
    """

    # TODO add proper error-handling methods

    @app.route("/sbom", methods=["POST"])
    def add_sbom():
        """
        Adds an SBOM to the database.

        Args:
             json (object): Object containing the SBOM data.
        """
        pass

    @app.route("/sbom", methods=["GET"])
    def get_sbom_names():
        """
        Gets the name of every SBOM in the database.

        Returns:
            json (array): The list of SBOM names.
        """
        pass

    @app.route("/sbom/<name>", methods=["GET"])
    def get_sboms_by_name(name: str):
        """
        Gets a list of SBOMs with a specific name.

        Args:
            name (str): The name to query the database with.

        Returns:
            json (array): The list of SBOMs.
        """
        pass

    @app.route("dependency/existing", methods=["GET"])
    def get_existing_dependencies():
        """
        Gets a list of dependencies, based on the specified primary
        keys.

        Args:
            json (array): The primary keys of the dependencies.

        Returns:
            json (array): The list of dependecies.
        """
        pass
