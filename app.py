# -*- coding: utf-8 -*-
"""Defining the REST API"""

import markdown
import pymatgen
import pytojcamp
from flask import Flask, abort, jsonify, request
from pymatgen import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pytojcamp import from_dict

app = Flask(__name__)


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

    try:
        structure = Structure.from_str(filecontent, fmt="cif")
    except Exception:  # pylint:disable=broad-except
        abort(500)

    wavelength = "CuKa"

    try:
        calculator = XRDCalculator(wavelength=wavelength)
        pattern = calculator.get_pattern(structure)
        two_theta = list(pattern.x)
        intensity = list(pattern.y)
        hkls = pattern.hkls

        output_dict = {
            "x": two_theta,
            "y": intensity,
            "hkls": hkls,
        }

        if return_jcamp:

            jcamp = from_dict(
                {
                    "x": {
                        "data": output_dict["x"],
                        "unit": "°",
                        "type": "INDEPENDENT",
                        "name": "2 theta",
                    },
                    "y": {
                        "data": output_dict["y"],
                        "type": "DEPENDENT",
                        "unit": "",
                        "name": "intensity",
                    },
                },
                data_type="Predicted PXRD pattern",
                origin=f"Pymatgen version {pymatgen.__version__}\
                     converted to JCAMP with pytojcamp version {pytojcamp.__version__}",
                meta={"wavelength": wavelength},
            )

            output_dict["jcamp"] = jcamp

        return jsonify(output_dict), 200

    except Exception:  # pylint:disable=broad-except
        abort(500)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
