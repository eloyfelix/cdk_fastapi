from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from starlette.requests import Request
from pydantic import BaseModel
from .java import *
import jpype


class Item(BaseModel):
    structure: str


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


@app.post("/smiles2molfile")
async def smi2mf(item: Item):
    molfile = smiles2molfile(item.structure)
    if molfile:
        return {"molfile": str(molfile)}
    else:
        raise HTTPException(
            status_code=500, detail=f"smilesToMolfile failed for {item.structure}"
        )


@app.post("/molfile2smiles")
async def mf2smi(item: Item):
    smiles = molfile2smiles(item.structure)
    if smiles:
        return {"smiles": str(smiles)}
    else:
        raise HTTPException(
            status_code=500, detail=f"molfile2smiles failed for {item.structure}"
        )


@app.post("/addHydrogens")
async def addHs(item: Item):
    smiles = addHydrogens(item.structure)
    if smiles:
        return {"smiles": str(smiles)}
    else:
        raise HTTPException(
            status_code=500, detail=f"removeHydrogens failed for {item.structure}"
        )


@app.post("/removeHydrogens")
async def removeHs(item: Item):
    smiles = removeHydrogens(item.structure)
    if smiles:
        return {"smiles": str(smiles)}
    else:
        raise HTTPException(
            status_code=500, detail=f"removeHydrogens failed for {item.structure}"
        )


@app.post("/addStereoelements")
async def addStereo(item: Item):
    smiles = addStereoelements(item.structure)
    if smiles:
        return {"smiles": str(smiles)}
    else:
        raise HTTPException(
            status_code=500, detail=f"addStereoelements failed for {item.structure}"
        )


@app.post("/depictSmiles")
async def depictSmiles(item: Item):
    svg = depict(item.structure)
    if svg:
        return {"svg": str(svg)}
    else:
        raise HTTPException(
            status_code=500, detail=f"depictSmiles failed for {item.structure}"
        )

@app.post("/opsin")
async def n2s(item: Item):
    smiles = name2structure(item.structure)
    if smiles:
        return {"smiles": str(smiles)}
    else:
        raise HTTPException(
            status_code=500, detail=f"opsin failed for {item.structure}"
        )
