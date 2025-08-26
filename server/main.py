import llm_client
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class AskRequest(BaseModel):
    provider: str
    prompt: str


@app.post("/ask")
def ask_endpoint(req: AskRequest):
    answer = llm_client.ask(req.provider, req.prompt)
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
