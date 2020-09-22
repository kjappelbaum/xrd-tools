from ... import app
import json 

with open("xalxuf01.cif", "r") as fh:
    f = fh.read()


def test_pxrd():
    response = app.test_client().post(
        "/api/predictxrd", structurefile=f, content_type="application/json",
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200

