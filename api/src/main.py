from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def newn():
    return {"u": "ahhh veryyy aey"}
