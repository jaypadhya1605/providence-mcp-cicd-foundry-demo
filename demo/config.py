from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


@dataclass(frozen=True)
class DemoConfig:
    subscription_id: str
    resource_group: str
    location: str
    foundry_account_name: str
    foundry_project_name: str
    foundry_project_endpoint: str
    foundry_model_deployment_name: str
    apim_service_name: str
    app_insights_name: str
    log_analytics_workspace: str
    content_understanding_account_name: str
    live_foundry_enabled: bool
    demo_environment: str

    @property
    def foundry_account_resource_id(self) -> str:
        return (
            f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}"
            f"/providers/Microsoft.CognitiveServices/accounts/{self.foundry_account_name}"
        )


def load_config() -> DemoConfig:
    values = _read_env_file(ROOT / ".env.template")
    values.update(_read_env_file(ROOT / ".env"))

    for key in list(values):
        values[key] = os.environ.get(key, values[key])

    def get(name: str, default: str = "") -> str:
        return os.environ.get(name, values.get(name, default))

    return DemoConfig(
        subscription_id=get("AZURE_SUBSCRIPTION_ID"),
        resource_group=get("AZURE_RESOURCE_GROUP"),
        location=get("AZURE_LOCATION", "eastus2"),
        foundry_account_name=get("FOUNDRY_ACCOUNT_NAME"),
        foundry_project_name=get("FOUNDRY_PROJECT_NAME"),
        foundry_project_endpoint=get("FOUNDRY_PROJECT_ENDPOINT"),
        foundry_model_deployment_name=get("FOUNDRY_MODEL_DEPLOYMENT_NAME"),
        apim_service_name=get("APIM_SERVICE_NAME"),
        app_insights_name=get("APP_INSIGHTS_NAME"),
        log_analytics_workspace=get("LOG_ANALYTICS_WORKSPACE"),
        content_understanding_account_name=get("CONTENT_UNDERSTANDING_ACCOUNT_NAME"),
        live_foundry_enabled=get("LIVE_FOUNDRY_ENABLED", "false").lower() == "true",
        demo_environment=get("DEMO_ENVIRONMENT", "dev"),
    )