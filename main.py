from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import uvicorn
from app.routes.run_chat import router as run_chat_router
from app.routes.run_report import router as run_report_router


load_dotenv()

app = FastAPI(title="AI_Tester", version="1.0.0", description="Tester for Real_estate_Agent")

app.include_router(run_chat_router, prefix="/chat")
app.include_router(run_report_router, prefix="/report")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as f:
        return f.read()

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
