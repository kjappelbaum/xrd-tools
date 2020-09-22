import requests
import sys

with open("xalxuf01.cif", "r") as fh:
    f = fh.read()


r = requests.post("http://localhost:8091/api/predictxrd/", data={"structurefile": f})
keys = r.json().keys()

if "x" in keys:
    print("PXRD prediction API works")
    sys.exit(0)
else:
    sys.exit(1)
