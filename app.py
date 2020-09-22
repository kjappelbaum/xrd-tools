from flask import Flask, jsonify, make_response, request, abort
from pymatgen import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator

app = Flask(__name__)


@app.route("/")
def index():
    return "We predict PXRD patterns"


# Todo: potentially also allow to request different light sources
@app.route("/api/predictxrd/", methods=["POST"])
def index(cif):
    if "structurefile" not in request.files:
        abort(400)

    structurefile = request.files["structurefile"]
    filecontent = structurefile.read().decode("utf-8")

    try:
        s = Structure.from_str(filecontent)
    except Exception:
        abort(512)

    try:
        calculator = XRDCalculator()
        pattern = calculator.get_pattern(s)
        x = list(pattern.x)
        y = list(pattern.y)
        hkls = pattern.hkls

        return jsonify({"x": x, "y": y, "hkls": hkls,}), 200

    except Exception:
        abort(513)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(513)
def could_not_calculate(error):
    return make_response(
        jsonify({"error": "Calculation of the XRD pattern failed"}), 502
    )


@app.errorhandler(512)
def could_not_read(error):
    return make_response(jsonify({"error": "Could not read structure file"}), 501)


if __name__ == "__main__":
    app.run(debug=True)
