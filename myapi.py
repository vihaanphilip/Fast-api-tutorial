from fastapi import FastAPI, Path
from typing import Optional

app = FastAPI()

# amazon.com/delete-user

# get own page  
@app.get("/")
def index():
    return {"name": "First Data"} 

students = {
    1: {
        "name": "john",
        "age": 17,
        "class": "year 12"
    },
}

# Path parameters
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(description="The ID of the student you want to view", gt=0, lt=3)):
    return students[student_id]

# Query parameters
@app.get("/get-by-name/")
def get_student(*, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}