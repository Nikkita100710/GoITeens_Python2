from fastapi import FastAPI

app = FastAPI()

# Список студентів
students = ["Микита", "Yaroslav", "Влад", "Матвей", "Діана", "Володя", "Владислав", "Василь", "Вальтер", "Вадим"]

soft_skills_teacher = "Анастасія Ivanchenko"
tech_skills_teacher = "Шарко Максим"


@app.get("/students/")
async def get_students():
    return {"students": students}

@app.get("/soft-skills-teacher/")
async def get_soft_skills_teacher():
    return {"soft_skills_teacher": soft_skills_teacher}

@app.get("/tech-skills-teacher/")
async def get_tech_skills_teacher():
    return {"tech_skills_teacher": tech_skills_teacher}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/name/{name}")
async def check_name(name: str):
    if len(name) > 12:
        return {"message": "Надто довге імя"}
    else:
        return {"message": f"{name}"}


@app.post("/post")
async def post_test(name: str):
    return {"message": f"{name}"}




@app.get("/HW")
async def get_hw(name: str):
    return await HW_(name)

async def HW_(name):
    return {"message": f"Hello, {name}"}

# http://127.0.0.1:8000/HW?name=John
# uvicorn P3_HW_0205_2024:app --reload
