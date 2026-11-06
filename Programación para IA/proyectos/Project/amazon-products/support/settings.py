"""Carga y validación de la configuración del modelo (config.json).
"""

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Settings(BaseModel):
    """Configuración del modelo de embeddings, validada desde config.json."""
    
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    #Campos
    model_name: str = Field(min_length=1) 
    batch_size: int = Field(gt=0, strict=True)
    device: Literal["cpu", "cuda", "mps"] = "cpu"

    # Validadores   
    @field_validator("model_name")
    @classmethod
    def require_nonblank_model_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("model_name no puede estar vacío ni ser solo espacios")
        return value

    @field_validator("batch_size", mode="before")
    @classmethod
    def reject_boolean_batch_size(cls, value: object) -> object:
        if isinstance(value, bool):
            raise ValueError("batch_size no puede ser un booleano")
        return value


def load_settings(path: Path) -> Settings:
    """Lee el archivo JSON de configuración y lo valida con el modelo Settings.
    """

    read = path.read_text(encoding="utf-8")
    data = json.loads(read)
    return Settings.model_validate(data)