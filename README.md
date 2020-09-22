# CIF tools webservice

REST-API built with flask that exposes [pymatgen](https://duckduckgo.com/?q=pymatgen&t=brave) functionality.

## Implemented methods

- `POST` to `/api/predictxrd` with `structurefile` data (CIF as string) returns:
  - `x`: with the 2 theta positions of the reflexes
  - `y`: intensity of the reflexes
  - `hkl` array of objects `{hkl: , multiplicity: }`
