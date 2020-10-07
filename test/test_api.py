# -*- coding: utf-8 -*-
"""Testing basic functionality of the API"""
import json
import sys

from app import app

sys.path.append("..")

with open("HKUST-1.cif", "r") as fh:
    f = fh.read()


def test_pxrd():
    """Test PXRD prediction"""
    response = app.test_client().post("/api/predictxrd/", data=dict(structurefile=f))
    data = json.loads(response.get_data(as_text=True))
    keys = data.keys()
    assert response.status_code == 200
    assert "x" in keys
    assert "y" in keys


def test_jcamp():
    """Test PXRD prediction with JCAMP return"""
    response = app.test_client().post(
        "/api/predictxrd/",
        data=dict(structurefile=f, jcamp="true"),
    )
    data = json.loads(response.get_data(as_text=True))
    keys = data.keys()
    assert response.status_code == 200
    assert "x" in keys
    assert "y" in keys
    assert "jcamp" in keys
