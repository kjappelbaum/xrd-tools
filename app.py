from flask import Flask, jsonify, make_response, request, abort
from pymatgen import Structure

app = Flask(__name__)


@app.route("/")
def index():
    return "We predict PXRD patterns"


@app.route("/api/predict/", methods=["POST"])
def index(cif):
    if "structurefile" not in request.files:
        abort(400)
    structurefile = request.files["structurefile"]

    filecontent = structurefile.read().decode("utf-8")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True)
