from fastapi import FastAPI

app = FastAPI(title="Maestro")


@app.get("/health")
def health():
    return {"status": "ok"}
