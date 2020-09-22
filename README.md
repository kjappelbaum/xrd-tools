# CIF tools webservice

![Docker Image Build and Test CI](https://github.com/cheminfo/xrd-tools/workflows/Docker%20Image%20Build%20CI/badge.svg)
![Python package](https://github.com/cheminfo/xrd-tools/workflows/Python%20package/badge.svg)

REST-API built with flask that exposes [pymatgen](https://duckduckgo.com/?q=pymatgen&t=brave) functionality.

## Implemented methods

- `GET` to `/` shows the `README.md`
- `POST` to `/api/predictxrd` with `structurefile` data (CIF as string) returns:
  - `x`: with the 2 theta positions of the reflexes
  - `y`: intensity of the reflexes
  - `hkl` array of objects `{hkl: , multiplicity: }`
