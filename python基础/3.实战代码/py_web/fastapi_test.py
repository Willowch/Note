from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def root():
    return {"message":"hello world"}

@app.get("/users")
def get_users():
    return [{"id":1,"name":"Alice","age":18},
            {"id":2,"name":"Bob","age":20}]

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)