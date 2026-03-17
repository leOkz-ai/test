import re
import json
from typing import Dict, List

def extract_project_data(text: str) -> Dict:
    data = {
        "project_type": "ai_service",
        "name": "AI‑система для автоматизации клиентских коммуникаций",
        "description": text[:1000].strip(),
        "features": [],
        "design_complexity": "medium",
        "backend_complexity": "medium",
        "frontend_complexity": "medium",
        "target_platforms": [],
        "integrations": [],
        "deadline_weeks": 20,
        "currency": "RUB",
        "similar_projects_found": 2
    }


    integration_map = {
        "amocrm": ["crm", "amo", "сделка", "статус клиента"],
        "1c": ["erp", "1с", "остатки", "цены", "синхронизация"],
        "payment_gateway": ["оплата", "qr", "онлайн‑платежи"],
        "telegram": ["telegram", "бот"],
        "whatsapp": ["whatsapp", "2gisa"],
        "avito": ["avito", "сайт компании"]
    }
    for sys, keys in integration_map.items():
        if any(k in text.lower() for k in keys) and sys not in data["integrations"]:
            data["integrations"].append(sys)


    platforms = ["web", "telegram", "whatsapp", "avito"]
    for p in platforms:
        if p in text.lower():
            data["target_platforms"].append(p)
    if not data["target_platforms"]:
        data["target_platforms"] = ["web"]


    feature_rules = [
        ("автоматическое создание и обновление сделок", "medium"),
        ("маршрутизация сообщений", "medium"),
        ("синхронизация прайсов", "high"),
        ("распознавание намерений", "high"),
        ("логирование действий", "low"),
        ("панель администрирования", "high"),
        ("мониторинг и метрики", "medium"),
        ("шифрование данных", "critical"),
        ("резервное копирование", "low"),
        ("интеграция с платежными системами", "critical")
    ]
    for phrase, complexity in feature_rules:
        if re.search(phrase, text, re.IGNORECASE):
            data["features"].append({"name": phrase, "complexity": complexity})


    high_words = ["критичный", "сложный", "высокая", "ответственный", "рискованный", "важный",
                 "требует контроля", "многокомпонентный", "масштабируемый"]
    medium_words = ["средний", "умеренный", "стандартный", "базовый"]


    high_count = sum(1 for w in high_words if w in text.lower())
    medium_count = sum(1 for w in medium_words if w in text.lower())


    if high_count >= 4:
        data["backend_complexity"] = "critical"
        data["design_complexity"] = "high"
    elif high_count >= 2:
        data["backend_complexity"] = "high"
        data["design_complexity"] = "medium"

    if medium_count >= 3:
        data["frontend_complexity"] = "medium"


    weeks_match = re.search(r"(\d+)\s*(недель|недели|неделю)", text)
    if weeks_match:
        weeks = int(weeks_match.group(1))
        if 4 <= weeks <= 104:
            data["deadline_weeks"] = weeks

    return data
