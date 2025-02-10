import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "student_db")
COLLECTION_NAME = "students"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
students_collection = db[COLLECTION_NAME]


def add(student=None):
    query = {"first_name": student.first_name, "last_name": student.last_name}
    res = students_collection.find_one(query)
    if res:
        return 'already exists', 409

    student_dict = student.to_dict()
    result = students_collection.insert_one(student_dict)
    student.student_id = str(result.inserted_id)
    return student.student_id


def get_by_id(student_id=None):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'not found', 404

    student['student_id'] = str(student['_id'])
    del student['_id']  # Remove MongoDB internal ID
    return student


def delete(student_id=None):
    result = students_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        return 'not found', 404
    return student_id

