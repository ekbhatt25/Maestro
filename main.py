from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="Maestro")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(audio: UploadFile = File(...)):
    return {
        "transcript": "stub",
        "features": {},
        "feedback": "stub feedback",
    }
