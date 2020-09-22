from flask import Flask, jsonify, make_response, request, abort
from pymatgen import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator

app = Flask(__name__)


@app.route("/")
def index():
    return "We predict PXRD patterns"


# Todo: potentially also allow to request different light sources
# ToDo: also provide file format
@app.route("/api/predictxrd/", methods=["POST"])
def predict():

    try:
        filecontent = request.form["structurefile"]

    except Exception:
        abort(400)

    try:
        s = Structure.from_str(filecontent, fmt="cif")
    except Exception:
        abort(500)

    try:
        calculator = XRDCalculator()
        pattern = calculator.get_pattern(s)
        x = list(pattern.x)
        y = list(pattern.y)
        hkls = pattern.hkls

        return jsonify({"x": x, "y": y, "hkls": hkls,}), 200

    except Exception:
        abort(500)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
