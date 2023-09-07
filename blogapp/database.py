from pymongo import MongoClient

uri = "mongodb://localhost:27017"
client = MongoClient(uri)
db = client["blogDB"]

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)