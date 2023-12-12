from fastapi import (
    APIRouter,
    Query,
    status, HTTPException
)
from starlette.requests import Request
from starlette.responses import JSONResponse

from .database_cows_functions import get_cows_by_field_from_db, get_cow_by_id_from_db, delete_cow_by_id_from_db, \
    is_unique_cow_in_db, create_cow_in_db, \
    update_cow_in_db
from .models import CowModel, CowUpdate
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/cows", response_model=list[CowModel])
async def get_cows(
        request: Request,
        name: str = Query(None, description="Cow's name"),
        sex: str = Query(None, description="Cow's sex"),
        condition: str = Query(None, description="Cow's condition")
) -> list[CowModel]:
    """Retrieve desired cow by name, sex or condition"""

    # initialize a dictionary that contains the fields to filter the cows by.
    filter_dict = {k: v for k, v in zip(["name", "sex", "condition"], [name, sex, condition]) if
                   v is not None}

    cows = await get_cows_by_field_from_db(request, filter_dict)

    return cows


@router.post("/cows", response_model=CowModel, status_code=status.HTTP_201_CREATED)
async def cows_post(request: Request, cow: CowModel):
    """Add cow to farm."""

    cow = jsonable_encoder(cow)
    cow_dict = {"name": cow["name"], "sex": cow["sex"], "birthdate": cow["birthdate"]}

    if (await get_cow_by_id_from_db(request, cow["_id"])) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cow ID already exists")

    if await is_unique_cow_in_db(request, cow_dict):
        new_cow = await create_cow_in_db(request, cow)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cow already exists")
    created_cow = await get_cow_by_id_from_db(request, new_cow.inserted_id)

    return created_cow


@router.get("/cows/{cow_id}", response_model=CowModel)
async def get_cow(request: Request, cow_id: str) -> CowModel:
    """Get Cow by id."""
    cow = await get_cow_by_id_from_db(request, cow_id)
    if cow is not None:
        return cow
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cow {cow_id} not found")


@router.put("/cows/{cow_id}", status_code=status.HTTP_200_OK, response_model=CowModel)
async def cows_put(request: Request, cow_id: str, cow_model: CowUpdate) -> CowModel:
    """Updates cow's details."""

    # exclude unset values from cow_model in order to update only the fields that are supposed to be updated.
    update_fields_dict = cow_model.dict(exclude_unset=True)
    # if the dictionary is of length over 0 then user provided fields to update the cow.
    if len(update_fields_dict) > 0:
        update_result = await update_cow_in_db(request, cow_id, update_fields_dict)

        # if there is a cow of the provided id then the value of modified_count should be 1.
        if update_result.modified_count == 1:
            if (updated_cow := await get_cow_by_id_from_db(request, cow_id)) is not None:
                return updated_cow
    elif (existing_cow := await get_cow_by_id_from_db(request, cow_id)) is not None:
        return existing_cow

    raise HTTPException(status_code=404, detail=f"Cow {cow_id} not found.")


@router.delete("/cows/{cow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cows_id_delete(request: Request, cow_id: str):
    """Delete cow from farm."""
    delete_result = await delete_cow_by_id_from_db(request, cow_id)

    if delete_result.deleted_count == 1:
        return JSONResponse(content=f"Cow {cow_id} Deleted!", status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cow {cow_id} not found!")
