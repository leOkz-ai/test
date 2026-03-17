from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from pathlib import Path

from aistart_with_llm import create_prompt, get_llm_response
import estimator_moduleF
from parser_agent import extract_project_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "example.db"
ESTIMATOR_CONFIG = BASE_DIR / "project_estimator.json"


@app.get("/")
def root():
    return {"message": "FastAPI работает"}


@app.get("/projects")
def get_projects():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, project_name, project_type, total_cost_rub,
               duration_weeks, team_size, generated_at
        FROM projects
        ORDER BY generated_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    projects = []
    for row in rows:
        projects.append({
            "id": str(row[0]),
            "name": row[1] or "Без названия",
            "client": row[2] or "—",
            "status": "active",
            "hours": row[4] or 0,
            "cost": row[3] or 0,
            "team_size": row[5] or 0,
            "generated_at": row[6] or ""
        })

    return projects


class ProjectInput(BaseModel):
    text: str


@app.post("/analyze")
def analyze_project(data: ProjectInput):
    try:
        project_data = extract_project_data(data.text)

        facade = estimator_moduleF.EstimationFacade(str(ESTIMATOR_CONFIG))
        result = facade.estimate_from_ai_input(project_data)

        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Ошибка расчёта")
            }

        estimate = result["data"]

        prompt = create_prompt(project_data, estimate)
        llm_response = get_llm_response(prompt)

        if not llm_response:
            llm_response = "Не удалось получить ответ от языковой модели."

        return {
            "success": True,
            "project_data": project_data,
            "estimate": estimate,
            "llm": llm_response
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }