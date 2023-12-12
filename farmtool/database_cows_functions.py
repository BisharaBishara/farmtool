from starlette.requests import Request
from .models import CowModel


async def get_cow_by_id_from_db(request: Request, cow_id: str):
    # convert id from str to ObjectId
    cow = await request.app.mongodb["Cows"].find_one({"_id": cow_id})

    return cow


async def get_cows_by_field_from_db(request: Request, filter_dict: dict):
    cows = []

    for cow in await request.app.mongodb["Cows"].find(filter_dict).to_list(1000):
        cows.append(cow)

    return cows


async def is_unique_cow_in_db(request: Request, cow_dict: dict) -> bool:

    cow = await request.app.mongodb["Cows"].find_one(cow_dict)

    return cow is None


async def create_cow_in_db(request: Request, cow: CowModel):

    cow = await request.app.mongodb["Cows"].insert_one(cow)

    return cow


async def update_cow_in_db(request: Request, cow_id: str, update_fields_dict: dict):

    # convert id from str to ObjectId
    update_result = await request.app.mongodb["Cows"].update_one(
        {"_id": cow_id}, {"$set": update_fields_dict}
    )

    return update_result


async def delete_cow_by_id_from_db(request: Request, cow_id: str):
    # convert id from str to ObjectId
    delete_result = await request.app.mongodb["Cows"].delete_one({"_id": cow_id})

    return delete_result
