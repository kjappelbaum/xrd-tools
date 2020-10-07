# CIF tools webservice

![Docker Image Build and Test CI](https://github.com/cheminfo/xrd-tools/workflows/Docker%20Image%20Build%20CI/badge.svg)
![Python package](https://github.com/cheminfo/xrd-tools/workflows/Python%20package/badge.svg)

REST-API built with flask that exposes [pymatgen](https://duckduckgo.com/?q=pymatgen&t=brave) functionality.

## Implemented methods

- `GET` to `/` shows the `README.md`
- `GET` to `/health` shows status information (for debugging)
- `POST` to `/api/predictxrd` with `structurefile` data (CIF as string) returns:

  - `x`: with the 2 theta positions of the reflexes
  - `y`: intensity of the reflexes
  - `hkl` array of objects `{hkl: , multiplicity: }`

  if you also provide `jcamp=true` you will receive

  - `jcamp`: a string of the JCAMP-DX file with the predicted pattern

  you can also specify a `wavelength` which must be one of the following strings: CuKa, CuKa2, CuKa1, CuKb1, MoKa, MoKa2, MoKa1, MoKb1, CrKa, CrKa2, CrKa1, CrKb1, FeKa, FeKa2, FeKa1, FeKb1, CoKa, CoKa2, CoKa1, CoKb1, AgKa, AgKa2, AgKa1, AgKb1.
