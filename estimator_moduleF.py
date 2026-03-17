import json
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field, field_validator, ConfigDict
from decimal import Decimal


class ProjectType(str, Enum):
    WEBSITE = "website"
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    ECOMMERCE = "ecommerce"
    MARKETPLACE = "marketplace"
    CRM = "crm"
    ERP = "erp"
    API = "api"
    CHATBOT = "chatbot"
    AI_SERVICE = "ai_service"
    OTHER = "other"


class ComplexityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RoleType(str, Enum):
    PROJECT_MANAGER = "project_manager"
    BUSINESS_ANALYST = "business_analyst"
    UX_UI_DESIGNER = "ux_ui_designer"
    FRONTEND_DEVELOPER = "frontend_developer"
    BACKEND_DEVELOPER = "backend_developer"
    FULLSTACK_DEVELOPER = "fullstack_developer"
    MOBILE_DEVELOPER = "mobile_developer"
    DEVOPS = "devops"
    QA_ENGINEER = "qa_engineer"
    DATA_SCIENTIST = "data_scientist"
    ML_ENGINEER = "ml_engineer"
    ARCHITECT = "architect"


class SeniorityLevel(str, Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"


class Feature(BaseModel):
    name: str
    complexity: ComplexityLevel
    description: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)

    def get_complexity_value(self) -> str:
        if isinstance(self.complexity, ComplexityLevel):
            return self.complexity.value
        return str(self.complexity)

class ProjectInput(BaseModel):
    project_type: ProjectType
    name: str
    description: str
    features: List[Feature] = Field(default_factory=list)
    design_complexity: ComplexityLevel
    backend_complexity: ComplexityLevel
    frontend_complexity: ComplexityLevel
    deadline_weeks: Optional[int] = Field(None, ge=1, le=104)
    budget_min_rub: Optional[Decimal] = Field(None, ge=0)
    budget_max_rub: Optional[Decimal] = Field(None, ge=0)
    target_platforms: List[str] = Field(default_factory=list)
    integrations: List[str] = Field(default_factory=list)
    currency: str = Field(default="RUB")

    model_config = ConfigDict(use_enum_values=True)

    @field_validator('budget_max_rub')
    @classmethod
    def validate_budget(cls, v, info):
        if v is not None and 'budget_min_rub' in info.data and info.data['budget_min_rub'] is not None:
            if v < info.data['budget_min_rub']:
                raise ValueError('budget_max_rub must be >= budget_min_rub')
        return v

    def get_project_type_value(self) -> str:
        if isinstance(self.project_type, ProjectType):
            return self.project_type.value
        return str(self.project_type)

    def get_design_complexity_value(self) -> str:
        if isinstance(self.design_complexity, ComplexityLevel):
            return self.design_complexity.value
        return str(self.design_complexity)

    def get_backend_complexity_value(self) -> str:
        if isinstance(self.backend_complexity, ComplexityLevel):
            return self.backend_complexity.value
        return str(self.backend_complexity)

    def get_frontend_complexity_value(self) -> str:
        if isinstance(self.frontend_complexity, ComplexityLevel):
            return self.frontend_complexity.value
        return str(self.frontend_complexity)


class RoleAssignment(BaseModel):
    role: RoleType
    role_name: str
    seniority: SeniorityLevel
    seniority_name: str
    hours: int = Field(ge=0, le=10000)
    count: int = Field(ge=1, le=20, default=1)
    rate_per_hour_rub: Decimal

    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)

    @property
    def total_hours(self) -> int:
        return self.hours * self.count

    @property
    def cost_rub(self) -> Decimal:
        return (self.rate_per_hour_rub * self.total_hours).quantize(Decimal('0.01'))

    def get_role_value(self) -> str:
        if isinstance(self.role, RoleType):
            return self.role.value
        return str(self.role)

    def get_seniority_value(self) -> str:
        if isinstance(self.seniority, SeniorityLevel):
            return self.seniority.value
        return str(self.seniority)

    def dict_for_json(self) -> dict:
        return {
            "role": self.get_role_value(),
            "role_name": self.role_name,
            "seniority": self.get_seniority_value(),
            "seniority_name": self.seniority_name,
            "hours": self.hours,
            "count": self.count,
            "total_hours": self.total_hours,
            "rate_per_hour_rub": float(self.rate_per_hour_rub),
            "cost_rub": float(self.cost_rub)
        }

def process_data(df):
    # Ваша логика обработки данных
    return df.describe()  # пример: возвращает статистику


class ProjectStage(BaseModel):
    name: str
    percentage: float
    cost_rub: Decimal
    duration_weeks: int

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def dict_for_json(self) -> dict:
        return {
            "name": self.name,
            "percentage": self.percentage,
            "cost_rub": float(self.cost_rub),
            "duration_weeks": self.duration_weeks
        }


class ProjectEstimate(BaseModel):
    total_cost_rub: Decimal
    total_hours: int
    duration_weeks: int
    team_size: int
    roles: List[RoleAssignment]
    hourly_rate_avg_rub: Decimal
    stages: Dict[str, ProjectStage]
    project_name: str
    project_type: str
    currency: str
    confidence_score: float = Field(ge=0, le=1.0)
    similar_projects_found: int
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def model_dump_for_json(self) -> dict:
        return {
            "total_cost_rub": float(self.total_cost_rub),
            "total_hours": self.total_hours,
            "duration_weeks": self.duration_weeks,
            "team_size": self.team_size,
            "roles": [role.dict_for_json() for role in self.roles],
            "hourly_rate_avg_rub": float(self.hourly_rate_avg_rub),
            "stages": {k: v.dict_for_json() for k, v in self.stages.items()},
            "project_name": self.project_name,
            "project_type": self.project_type,
            "currency": self.currency,
            "confidence_score": self.confidence_score,
            "similar_projects_found": self.similar_projects_found,
            "created_at": self.created_at.isoformat()
        }


class ConfigLoader:
    def __init__(self, config_path: str = "project_estimator.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            self.config_path = os.path.join(os.path.dirname(__file__), "project_estimator.json")

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Конфигурационный файл {self.config_path} не найден.")

    @property
    def currency(self) -> str:
        return self.config['metadata'].get('currency', 'RUB')

    def get_project_type_base_hours(self, project_type: str) -> int:
        return self.config['project_types'].get(project_type, {}).get('base_hours', 200)

    def get_project_type_name(self, project_type: str) -> str:
        return self.config['project_types'].get(project_type, {}).get('name', project_type)

    def get_role_name(self, role: str) -> str:
        return self.config['roles'].get(role, {}).get('name', role)

    def get_seniority_name(self, seniority: str) -> str:
        return self.config['seniority_levels'].get(seniority, {}).get('name', seniority)

    def get_complexity_multiplier(self, complexity: str) -> float:
        return self.config['complexity_levels'].get(complexity, {}).get('multiplier', 1.0)

    def get_rate_rub(self, role: str, seniority: str) -> Decimal:
        rate_card = self.config['rate_card_rub']
        role_rates = rate_card.get(role, {})
        rate = role_rates.get(seniority)

        if rate is None:
            if seniority in ['junior', 'middle'] and role == 'architect':
                rate = role_rates.get('senior', 8100)
            else:
                rate = role_rates.get('middle', 3600)

        return Decimal(str(rate))

    def get_role_distribution(self, project_type: str) -> Dict[str, float]:
        return self.config['role_distribution'].get(project_type,
                                                    self.config['role_distribution']['other'])

    def get_seniority_distribution(self, complexity: str) -> Dict[str, float]:
        return self.config['seniority_distribution'].get(complexity,
                                                         self.config['seniority_distribution']['medium'])

    def get_project_stages(self) -> Dict[str, dict]:
        return self.config['project_stages']

    def get_confidence_factors(self) -> dict:
        return self.config['confidence_factors']

    def get_calculation_rules(self) -> dict:
        return self.config['calculation_rules']


class ProjectEstimator:
    def __init__(self, config_path: str = "project_estimator.json"):
        self.config = ConfigLoader(config_path)

    def estimate(self, project_input: ProjectInput,
                 similar_projects_count: int = 0) -> ProjectEstimate:
        base_hours = self._calculate_base_hours(project_input)
        total_hours = self._apply_complexity(base_hours, project_input)
        overall_complexity = self._determine_overall_complexity(project_input)

        role_assignments = self._distribute_roles(
            total_hours,
            project_input.get_project_type_value(),
            overall_complexity
        )

        total_cost_rub = Decimal('0')
        for assignment in role_assignments:
            total_cost_rub += assignment.cost_rub

        duration_weeks, team_size = self._calculate_timeline(
            role_assignments,
            project_input.deadline_weeks
        )

        if total_hours > 0:
            avg_rate_rub = total_cost_rub / Decimal(str(total_hours))
        else:
            avg_rate_rub = Decimal('0')

        stages = self._generate_stages(project_input, total_cost_rub)
        confidence = self._calculate_confidence(project_input, similar_projects_count)

        return ProjectEstimate(
            total_cost_rub=total_cost_rub.quantize(Decimal('0.01')),
            total_hours=total_hours,
            duration_weeks=duration_weeks,
            team_size=team_size,
            roles=role_assignments,
            hourly_rate_avg_rub=avg_rate_rub.quantize(Decimal('0.01')),
            stages=stages,
            project_name=project_input.name,
            project_type=project_input.get_project_type_value(),
            currency=project_input.currency,
            confidence_score=confidence,
            similar_projects_found=similar_projects_count
        )

    def _calculate_base_hours(self, project_input: ProjectInput) -> int:
        rules = self.config.get_calculation_rules()
        base = self.config.get_project_type_base_hours(project_input.get_project_type_value())
        feature_base = rules.get('feature_base_hours', 20)

        feature_hours = 0
        for feature in project_input.features:
            multiplier = self.config.get_complexity_multiplier(feature.get_complexity_value())
            feature_hours += int(feature_base * multiplier)

        return base + feature_hours

    def _apply_complexity(self, hours: int, project_input: ProjectInput) -> int:
        multipliers = [
            self.config.get_complexity_multiplier(project_input.get_design_complexity_value()),
            self.config.get_complexity_multiplier(project_input.get_backend_complexity_value()),
            self.config.get_complexity_multiplier(project_input.get_frontend_complexity_value())
        ]
        avg_multiplier = sum(multipliers) / len(multipliers)
        return int(hours * avg_multiplier)

    def _determine_overall_complexity(self, project_input: ProjectInput) -> str:
        complexities = [
            project_input.get_design_complexity_value(),
            project_input.get_backend_complexity_value(),
            project_input.get_frontend_complexity_value()
        ]

        if ComplexityLevel.CRITICAL.value in complexities:
            return ComplexityLevel.CRITICAL.value

        high_count = complexities.count(ComplexityLevel.HIGH.value)
        if high_count >= 2:
            return ComplexityLevel.HIGH.value

        if ComplexityLevel.HIGH.value in complexities:
            return ComplexityLevel.HIGH.value

        return ComplexityLevel.MEDIUM.value

    def _distribute_roles(self, total_hours: int, project_type: str,
                          overall_complexity: str) -> List[RoleAssignment]:
        distribution = self.config.get_role_distribution(project_type)
        seniority_dist = self.config.get_seniority_distribution(overall_complexity)

        assignments = []

        for role, percentage in distribution.items():
            role_hours = int(total_hours * percentage)
            for seniority, seniority_percent in seniority_dist.items():
                if seniority_percent > 0 and role_hours > 0:
                    seniority_hours = int(role_hours * seniority_percent)
                    if seniority_hours > 0:
                        rate_rub = self.config.get_rate_rub(role, seniority)
                        assignments.append(
                            RoleAssignment(
                                role=RoleType(role),
                                role_name=self.config.get_role_name(role),
                                seniority=SeniorityLevel(seniority),
                                seniority_name=self.config.get_seniority_name(seniority),
                                hours=seniority_hours,
                                count=1,
                                rate_per_hour_rub=rate_rub
                            )
                        )
        return assignments

    def _calculate_timeline(self, role_assignments: List[RoleAssignment],
                            deadline_weeks: Optional[int] = None) -> Tuple[int, int]:
        rules = self.config.get_calculation_rules()
        hours_per_week = rules.get('hours_per_week', 40)

        total_person_hours = sum(a.total_hours for a in role_assignments)
        unique_roles = len(set(a.get_role_value() for a in role_assignments))

        if deadline_weeks:
            hours_per_week_needed = total_person_hours / deadline_weeks
            team_size = max(unique_roles, int(hours_per_week_needed / hours_per_week) + 1)
            return deadline_weeks, team_size
        else:
            weeks = int(total_person_hours / (hours_per_week * unique_roles)) + 1
            return weeks, unique_roles

    def _generate_stages(self, project_input: ProjectInput,
                         total_cost_rub: Decimal) -> Dict[str, ProjectStage]:
        stages_config = self.config.get_project_stages()
        stages = {}
        for stage_id, stage_data in stages_config.items():
            percentage = stage_data['percentage']
            stages[stage_id] = ProjectStage(
                name=stage_data['name'],
                percentage=percentage,
                cost_rub=(total_cost_rub * Decimal(str(percentage))).quantize(Decimal('0.01')),
                duration_weeks=stage_data['duration_weeks']
            )
        return stages

    def _calculate_confidence(self, project_input: ProjectInput,
                              similar_projects: int) -> float:
        factors = self.config.get_confidence_factors()
        confidence = factors.get('base_confidence', 0.5)
        per_project = factors.get('per_similar_project', 0.05)
        max_boost = factors.get('max_similar_projects_boost', 0.3)
        confidence += min(max_boost, similar_projects * per_project)

        if project_input.deadline_weeks:
            confidence += factors.get('deadline_boost', 0.1)
        if project_input.budget_min_rub and project_input.budget_max_rub:
            confidence += factors.get('budget_boost', 0.1)

        return min(1.0, confidence)


class EstimationFacade:
    def __init__(self, config_path: str = "project_estimator.json"):
        self.estimator = ProjectEstimator(config_path)
        self.config = ConfigLoader(config_path)

    def estimate_from_ai_input(self, ai_json_input: dict) -> dict:
        try:
            if 'currency' not in ai_json_input:
                ai_json_input['currency'] = self.config.currency

            project_input = ProjectInput(**ai_json_input)
            similar_projects = ai_json_input.get('similar_projects_found', 0)
            estimate = self.estimator.estimate(project_input, similar_projects)

            return {
                "success": True,
                "data": estimate.model_dump_for_json(),
                "message": "Расчёт успешно выполнен"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Ошибка при расчёте проекта"
            }


def example_usage():
    facade = EstimationFacade("project_estimator.json")

    ai_input = {
        "project_type": "ecommerce",
        "name": "Маркетплейс для фермерских продуктов",
        "description": "Платформа где фермеры могут продавать продукты напрямую покупателям",
        "design_complexity": "medium",
        "backend_complexity": "high",
        "frontend_complexity": "medium",
        "features": [
            {"name": "Аутентификация и профили", "complexity": "medium"},
            {"name": "Каталог товаров с фильтрацией", "complexity": "high"},
            {"name": "Корзина и оформление заказа", "complexity": "high"},
            {"name": "Интеграция с платежными системами", "complexity": "critical"},
            {"name": "Личный кабинет продавца", "complexity": "high"},
            {"name": "Система рейтингов и отзывов", "complexity": "medium"},
            {"name": "Админ-панель", "complexity": "medium"},
            {"name": "Мобильная адаптация", "complexity": "medium"}
        ],
        "target_platforms": ["web", "mobile"],
        "integrations": ["payment_gateways", "crm", "email_service"],
        "deadline_weeks": 16,
        "currency": "RUB",
        "similar_projects_found": 5
    }

    result = facade.estimate_from_ai_input(ai_input)

    if result["success"]:
        estimate = result["data"]
        print("=" * 70)
        print("РЕЗУЛЬТАТ РАСЧЁТА ПРОЕКТА")
        print("=" * 70)
        print(f"Проект: {estimate['project_name']}")
        print(f"Тип: {estimate['project_type']}")
        print(f"Общая стоимость: {estimate['total_cost_rub']:,.2f} ₽")
        print(f"Общее количество часов: {estimate['total_hours']}")
        print(f"Длительность: {estimate['duration_weeks']} недель")
        print(f"Размер команды: {estimate['team_size']} человек")
        print(f"Средняя ставка: {estimate['hourly_rate_avg_rub']:.0f} ₽/час")
        print(f"Достоверность оценки: {estimate['confidence_score'] * 100:.0f}%")

        print("\n--- РАСПРЕДЕЛЕНИЕ ПО РОЛЯМ ---")
        for role in estimate['roles']:
            print(f"{role['role_name']} ({role['seniority_name']}): "
                  f"{role['total_hours']} часов, {role['count']} чел., "
                  f"{role['cost_rub']:,.0f} ₽")

        print("\n--- ЭТАПЫ ПРОЕКТА ---")
        for stage, data in estimate['stages'].items():
            print(f"{data['name']}: {data['cost_rub']:,.0f} ₽ ({data['duration_weeks']} нед.)")

        with open('../project_estimate.json', 'w', encoding='utf-8') as f:
            json.dump(estimate, f, ensure_ascii=False, indent=2)

        print("\n✅ Детальный расчёт сохранён в project_estimate.json")
    else:
        print(f"❌ Ошибка: {result['error']}")


if __name__ == "__main__":
    example_usage()