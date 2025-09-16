import motor.motor_asyncio

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "assessment_db"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# employees collection
employees_collection = db["employees"]
