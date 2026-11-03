from pymongo import AsyncMongoClient

from .coonfig import settings

mongodb_client= AsyncMongoClient(settings.MONGODB_URL)
events_collection = mongodb_client[settings.MONGODB_DATABASE][settings.MONGODB_COLLECTION]
