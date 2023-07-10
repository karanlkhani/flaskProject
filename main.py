from flask import Flask
from flask import request
import json

app = Flask(__name__)

studentsDetails = []

def load_student_details():
     file = open("studentDetails.json","r")
     students = json.load(file)
     file.close()
     return students["studentsDetails"]
     
def save_student_details(inputJson):
    file = open("studentDetails.json", "w")
    json.dump(inputJson, file)
    file.close()
    return True

studentsDetails = load_student_details()
     
@app.route("/",methods=['GET'])
def defaultFunction():
        return "invalid route"

@app.route("/addUser",methods = ['POST'])
def addUser():
    if request.method == 'POST':
        studentsDetailsArray = load_student_details()
        req = request.get_json()
        
        for student in studentsDetailsArray:
             if req["rollnumber"] == student["rollnumber"]:
               return {"status":400,"message":"Rollnumber already exists"}
        else:
            studentsDetailsArray.append(req)
        if(save_student_details({"studentsDetails":studentsDetailsArray})):
            return {"status":200,"message":"Added Sucessfull","data":studentsDetailsArray}

@app.route("/getAllUsers",methods=['GET'])
def getAllUser():
      if request.method == 'GET':
        return json.dumps({"data":load_student_details(),"status":200})

@app.route("/deleteUser", methods=["DELETE"])
def deleteUser():
    if request.method == "DELETE":
        requestBody = request.get_json()
        tails = load_student_details()
        for student in tails:
                if requestBody["rollnumber"] == student["rollnumber"]:
                    tails.remove(student)
                save_student_details({"studentsDetails":tails})
                return json.dumps({"data":load_student_details(),"status":200})
    return ("Student not found ")

@app.route("/UpdateUser", methods=["PUT"])
def UpdateUser():
    if request.method == "PUT":
        requested = request.get_json()
        reqest = requested["rollnumber"]
        details = load_student_details()
        for student in details: 
            if reqest == student["rollnumber"]:
                student["name"] = requested["name"]
                student["age"] = requested["age"]
                student["grade"] = requested["grade"]
                student["section"] = requested["section"]
                save_student_details({"studentsDetails": details})
                return json.dumps({"status": 200, "message": "Update Successful"})
        return json.dumps({"status": 400, "message": "Incorrect roll number entered"})
    else:
        return json.dumps({"status": 400, "message": "Invalid method"})


@app.route("/SearchUser", methods = ["GET"])
def SearchUser():
     if request.method == "GET":
        data = request.get_json()
        data2 = data["rollnumber"]
        det = load_student_details()
        for student in det:
            if data2 == student["rollnumber"]:
                return json.dumps({"data": student, "status":200})
        
        return json.dumps({"message":"RollNumber not found", "status" : 401})

if __name__ == "__main__":
	 app.run(host="127.0.0.9", port=8080,debug=True)

