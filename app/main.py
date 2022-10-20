from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from starlette.requests import Request
from pydantic import BaseModel
from typing import Optional
from .java import *
import jpype


class Structure(BaseModel):
    structure: str
    gen_coords: Optional[bool] = False

class Depict(BaseModel):
    structure: str
    heigth: Optional[int] = 50
    width: Optional[int] = 50
    gen_coords: Optional[bool] = False

class Convert(BaseModel):
    structure: str
    out_format: str
    gen_coords: Optional[bool] = False


app = FastAPI()


@app.middleware("http")
async def attachThreadToJVM_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    if not jpype.isThreadAttachedToJVM():
        jpype.attachThreadToJVM()
    try:
        response: Response = await call_next(request)
    finally:
        pass
    return response


@app.post("/convert")
async def convert(item: Convert):
    structure = convert_mol(item)
    if structure:
        return {"structure": str(structure)}
    else:
        raise HTTPException(
            status_code=500, detail=f"convert failed for {item.structure}"
        )


@app.post("/addHydrogens")
async def addHydrogens(item: Structure):
    structure = add_hydrogens(item)
    if structure:
        return {"structure": str(structure)}
    else:
        raise HTTPException(
            status_code=500, detail=f"addHydrogens failed for {item.structure}"
        )


@app.post("/removeHydrogens")
async def removeHydrogens(item: Structure):
    structure = remove_hydrogens(item)
    if structure:
        return {"structure": str(structure)}
    else:
        raise HTTPException(
            status_code=500, detail=f"removeHydrogens failed for {item.structure}"
        )


@app.post("/addStereoElements")
async def addStereoElements(item: Structure):
    structure = add_stereo_elements(item)
    if structure:
        return {"structure": str(structure)}
    else:
        raise HTTPException(
            status_code=500, detail=f"addStereoElements failed for {item.structure}"
        )


@app.post("/depict")
async def depict(item: Depict):
    svg = depict_image(item)
    if svg:
        return {"svg": str(svg)}
    else:
        raise HTTPException(
            status_code=500, detail=f"depict failed for {item.structure}"
        )


@app.post("/molFormula")
async def molFormula(item: Structure):
    mol_formula = calculate_formula(item)
    if mol_formula:
        return {"molFormula": str(mol_formula)}
    else:
        raise HTTPException(
            status_code=500, detail=f"molFormula failed for {item.structure}"
        )


@app.post("/name2structure")
async def name2structure(item: Structure):
    smiles = name_to_structure(item.structure)
    if smiles:
        return {"smiles": str(smiles)}
    else:
        raise HTTPException(
            status_code=500, detail=f"name2structure failed for {item.structure}"
        )
