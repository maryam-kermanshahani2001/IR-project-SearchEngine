import traceback

import uvicorn
from fastapi import FastAPI
from search_engine import SearchEngine

app = FastAPI()


@app.get("/")
def test():
    return "This is the IR project"


@app.get("/api/engine/{user_query}")
async def process(user_query: str):
    try:
        return engine.execute(user_query)
    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    engine = SearchEngine()
    uvicorn.run(app, host="localhost", port=5051)
