from typing import Optional, List

import fastapi
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

router = fastapi.APIRouter()


@router.get("/sections")
async def get_read_sections():
    return {"sections": []}


@router.post("/sections")
async def create_section_api():
    return {"sections": []}


@router.get("/sections/{id}")
async def get_section(id: int):
    return {"sections": []}


@router.patch("/sections/{id}")
async def update_section(id: int):
    return {"sections": []}


@router.delete("/sections/{id}")
async def delete_section(id: int):
    return {"sections": []}
