import sys

sys.path.append("..")
from app import app
import json

with open("xalxuf01.cif", "r") as fh:
    f = fh.read()


def test_pxrd():
    response = app.test_client().post("/api/predictxrd/", data=dict(structurefile=f))
    data = json.loads(response.get_data(as_text=True))
    keys = data.keys()
    assert response.status_code == 200
    assert "x" in keys
    assert "y" in keys
