import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DB = config("MONGO")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB)

database = client.notes

user_collection = database.get_collection("users")


def formatter(user):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "age": user["age"],
        "notes": user["notes"]
    }


async def retrieve_users():
    return [formatter(user) async for user in user_collection.find()]


async def add_user(data: dict) -> dict:
    user = await user_collection.insert_one(data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})

    return formatter(new_user)


async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})  # Empty if user doesnt exist

    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})


async def retrieve_user(id: str):

    user = await user_collection.find_one({"_id": ObjectId(id)})

    if user:
        return formatter(user)


async def update_user(id: str, data: dict):

    # if data is empty, return none
    if not data:
        return False

    user = await user_collection.find_one({"_id": ObjectId(id)})

    if user:
        await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        updated_user = await user_collection.find_one({"_id": ObjectId(id)})

        return formatter(updated_user)
