from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"data": {"name": "Alex", "age": 36, "spec": "Python developer"}}


@app.get("/about")
def about():
    return {"data": "This is about page :)"}
