
import motor.motor_asyncio
from dotenv import dotenv_values
from pydantic import BeforeValidator
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

config = dotenv_values(".env")
print(config)
client = motor.motor_asyncio.AsyncIOMotorClient(config["DB_URL"])
db = client.get_database(config["MONGO_DB"])
# student_collection = db.get_collection("students")
# ipn_collection = db.get_collection("ipn")
# ipn_url_collection = db.get_collection("ipn_url")
# tax_collection = db.get_collection("tax_info")
# key_collection = db.get_collection("key_info")
