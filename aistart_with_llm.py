import json
from datetime import datetime
import estimator_moduleF
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from parser_agent import extract_project_data
import traceback
import sqlite3
import os




def init_db():
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                project_type TEXT,
                total_cost_rub REAL,
                duration_weeks INTEGER,
                team_size INTEGER,
                generated_at TEXT,
                input_project TEXT,
                estimation TEXT,
                llm_analysis TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("База данных инициализирована: example.db")
    except Exception as e:
        print(f'Ошибка при инициализации: {e}')
        traceback.print_exc()


def save_to_db(project_data, estimate, llm_response):
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO projects (
                project_name, project_type, total_cost_rub, duration_weeks,
                team_size, generated_at, input_project, estimation, llm_analysis
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            estimate['project_name'],
            estimate['project_type'],
            estimate['total_cost_rub'],
            estimate['duration_weeks'],
            estimate['team_size'],
            datetime.now().isoformat(),
            json.dumps(project_data, ensure_ascii=False),
            json.dumps(estimate, ensure_ascii=False),
            llm_response
        ))

        conn.commit()
        conn.close()
        print("✅ Отчёт сохранён в бд")
    except Exception as e:
        print(f"При сохранении произошла ошибка: {e}")
        traceback.print_exc()


def show_all_project():
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, project_name, generated_at FROM projects ORDER BY generated_at DESC")
        projects = cursor.fetchall()
        conn.close()

        if projects:
            print("Сохранённые проекты в БД:")
            for p in projects:
                print(f"  #{p[0]} {p[1]} ({p[2]})")
        else:
            print("\nВ БД пусто")
    except Exception as e:
        print(f'Ошибка при чтении БД: {e}')
        traceback.print_exc()


def create_prompt(project_data: dict, estimate: dict) -> str:
    features_list = "\n".join([f"  • {f['name']} ({f['complexity']})" for f in project_data["features"]])
    roles_list = "\n".join([
        f"  • {r['role_name']} ({r['seniority_name']}): {r['total_hours']} ч, {r['cost_rub']:,.0f} ₽"
        for r in estimate["roles"]
    ])
    stages_list = "\n".join([
        f"  • {s['name']}: {s['cost_rub']:,.0f} ₽ ({s['duration_weeks']} нед.)"
        for s in estimate["stages"].values()
    ])

    return f"""
Вы — эксперт по оценке IT-проектов. Данные:

ПРОЕКТ:
- Название: {project_data['name']}
- Тип: {project_data['project_type']}
- Описание: {project_data['description']}
- Сроки: {project_data['deadline_weeks']} недель
- Валюта: {project_data['currency']}
- Аналоги: {project_data['similar_projects_found']}

ОСОБЕННОСТИ:
{features_list}

РАСЧЁТ:
- Стоимость: {estimate['total_cost_rub']:,.0f} ₽
- Время: {estimate['total_hours']} ч
- Длительность: {estimate['duration_weeks']} нед.
- Команда: {estimate['team_size']} чел.
- Средняя ставка: {estimate['hourly_rate_avg_rub']:,.0f} ₽/ч
- Достоверность: {estimate['confidence_score']:.0%}


РОЛИ:
{roles_list}

ЭТАПЫ:
{stages_list}

Задайте:
1. Суть проекта (1–2 предл.).
2. 3–5 рисков.
3. 3–4 рекомендации по оптимизации.
4. Оценка реалистичности сроков.
5. Вывод (1 предл.).


Отвечайте списком, без вступлений.
"""


def get_llm_response(prompt: str):
    try:
        llm = OllamaLLM(model="qwen3:8b", base_url="http://127.0.0.1:11434", temperature=0.3)
        chain = ChatPromptTemplate.from_template("{input}") | llm
        response = chain.invoke({"input": prompt})
        return str(response).strip()
    except Exception as e:
        print(f"❌ Ошибка при вызове LLM: {e}")
        traceback.print_exc()
        return None


def save_report(project_data, estimate, llm_response):
    report = {
        "input_project": project_data,
        "estimation": estimate,
        "llm_analysis": llm_response,
        "generated_at": datetime.now().isoformat()
    }
    try:
        with open("report_with_llm.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print("✅ Отчёт сохранён: report_with_llm.json")
    except IOError as e:
        print(f"❌ Ошибка при сохранении отчёта: {e}")
        traceback.print_exc()


def main():
    try:
        init_db()

        show_all_project()

        if not os.path.exists("project_description.txt"):
            print("❌ Файл project_description.txt не найден!")
            return

        with open("project_description.txt", "r", encoding="utf-8") as f:
            text = f.read()

        project_data = extract_project_data(text)
        print("✅ Данные извлечены:", json.dumps(project_data, indent=2, ensure_ascii=False))

        facade = estimator_moduleF.EstimationFacade("project_estimator.json")
        result = facade.estimate_from_ai_input(project_data)

        if not result["success"]:
            print("❌ Ошибка расчёта:", result["error"])
            return

        estimate = result["data"]
        print("✅ Расчёт готов")

        # Получение ответа от LLM
        prompt = create_prompt(project_data, estimate)
        llm_response = get_llm_response(prompt)
        if llm_response:
            print("✅ Ответ LLM получен")
        else:
            print("⚠️ Ответ LLM пустой или не получен")
            llm_response = "Не удалось получить ответ от языковой модели."

        save_report(project_data, estimate, llm_response)
        save_to_db(project_data, estimate, llm_response)

        # Вывод итогов в консоль
        print("\n" + "=" * 60)
        print("ИТОГ: КРАТКИЙ ОБЗОР")
        print("=" * 60)
        print(f"Проект: {estimate['project_name']}")
        print(f"Тип: {estimate['project_type']}")
        print(f"Общая стоимость: {estimate['total_cost_rub']:,.2f} ₽")
        print(f"Общее количество часов: {estimate['total_hours']}")
        print(f"Длительность: {estimate['duration_weeks']} недель")
        print(f"Размер команды: {estimate['team_size']} человек")
        print(f"Средняя ставка: {estimate['hourly_rate_avg_rub']:,.0f} ₽/час")
        print(f"Достоверность оценки: {estimate['confidence_score']:.0%}")

        print("\n--- РАСПРЕДЕЛЕНИЕ ПО РОЛЯМ ---")
        for role in estimate['roles']:
            print(f"{role['role_name']} ({role['seniority_name']}): "
                  f"{role['total_hours']} часов, {role['count']} чел., {role['cost_rub']:,.0f} ₽")

        print("\n--- ЭТАПЫ ПРОЕКТА ---")
        for stage_name, stage in estimate['stages'].items():
            print(f"{stage_name}: {stage['cost_rub']:,.0f} ₽ ({stage['duration_weeks']} нед.)")

        print("\n🔍 Анализ LLM:")
        print("-" * 60)
        print(llm_response)

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
