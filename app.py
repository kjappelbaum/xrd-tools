# -*- coding: utf-8 -*-
"""Defining the REST API"""

import logging
import os

import markdown
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from pymatgen import Structure

from xrd_tools import calculate_pattern

app = Flask(__name__)
CORS(app)

gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)  # pylint:disable=no-member


@app.route("/health", methods=["GET"])
def get_status():
    """For debugging"""
    app.logger.info("checking health of application")  # pylint:disable=no-member
    return jsonify({"status": "UP"}), 200


@app.route("/")
def index():
    """Shows the documentation"""
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string


# Todo: potentially also allow to request different light sources
# ToDo: also provide file format
@app.route("/api/predictxrd/", methods=["POST"])
def predictxrd():
    """Predicting a PXRD pattern"""
    try:
        filecontent = request.form["structurefile"]

    except Exception:  # pylint:disable=broad-except
        abort(400)

    try:
        return_jcamp = (
            True  # pylint:disable= simplifiable-if-expression
            if request.form["jcamp"] == "true"
            else False
        )
    except Exception:  # pylint:disable=broad-except
        return_jcamp = False

    extension = "cif"
    try:
        if request.form["extension"] in ["cif"]:
            extension = request.form["extension"]
    except Exception:  # pylint:disable=broad-except
        pass

    try:
        structure = Structure.from_str(filecontent, fmt=extension)
    except Exception:  # pylint:disable=broad-except
        abort(500, "Could not read structure")

    wavelength = "CuKa"

    try:
        output_dict = calculate_pattern(structure, wavelength, return_jcamp)
        return jsonify(output_dict), 200
    except TimeoutError:
        abort(408)
    except Exception:  # pylint:disable=broad-except
        abort(500)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
