from flask import Flask
from flask import request
import json
from pymongo import MongoClient


app = Flask(__name__)

studentsDetails = []
client = MongoClient("mongodb://localhost:27017")
db = client["newdoc"]
collection = db["students"]
 
     
@app.route("/",methods=['GET'])
def defaultFunction():
        return "invalid route"

@app.route("/addUser",methods = ['POST'])
def addUser():
    if request.method == 'POST':
        req = request.get_json()
        rollnumber = req["rollnumber"]
        if collection.find_one({"rollnumber":rollnumber}):
               return json.dumps({"status":400,"message":"Rollnumber already exists"})
        else:
            collection.insert_one(req)
            return json.dumps({"status":200,"message":"Added Sucessfull","data":req}, default=str)

@app.route("/getAllUsers",methods=['GET'])
def getAllUser():
      if request.method == 'GET':
           users = list(collection.find())
           return json.dumps({"data":users,"status":200}, default=str)
      

@app.route("/deleteUser", methods=["DELETE"])
def deleteUser():
    if request.method == "DELETE":
        requestBody = request.get_json()
        tails = requestBody["rollnumber"]
        if  collection.find_one({"rollnumber":tails}):
            collection.delete_one({"rollnumber":tails})
            return json.dumps({"messsage":"Deleted Successfully","status":200})
    return ("Student not found ")

@app.route("/UpdateUser", methods=["PUT"])
def UpdateUser():
    if request.method == "PUT":
        requested = request.get_json()
        reqest = requested["rollnumber"]
         
        if collection.find_one({"rollnumber":reqest}):
            collection.update_one({"rollnumber":reqest},{"$set":requested})
            return json.dumps({"status": 200, "message": "Update Successful"})
        
        return json.dumps({"status": 400, "message": "Incorrect roll number entered"})
    else:
        return json.dumps({"status": 400, "message": "Invalid method"})


@app.route("/SearchUser", methods = ["GET"])
def SearchUser():
     if request.method == "GET":
        data = request.get_json()
        data2 = data["rollnumber"]
        student = collection.find_one({"rollnumber":data2})
        if student:
             return json.dumps({"data": student, "status":200},default=str)
        return json.dumps({"message":"RollNumber not found", "status" : 401})

if __name__ == "__main__":
	 app.run(host="127.0.0.9", port=8080,debug=True)

