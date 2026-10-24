"""Carga y validación de la configuración del modelo (config.json).

Patrón de referencia: notebook u1_n3_tipado_pydantic, sección 6 (BatchConfig).
La configuración gobierna todo el procesamiento, así que validamos de inmediato
(fail-fast): si es inválida, el servidor no debe arrancar.
"""

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Settings(BaseModel):
    """Configuración del modelo de embeddings, validada desde config.json."""

    # extra="forbid": rechaza claves desconocidas (p. ej. un typo en config.json).
    # validate_assignment=True: revalida si alguien reasigna un campo después.
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    # --- Campos ---
    # TODO (1): model_name debe ser un str con al menos 1 carácter.
    #           Usa Field(min_length=1). Mira cómo BatchConfig declaró batch_name.
    model_name: str = Field(min_length=1) 
    
    # TODO (2): batch_size debe ser un entero POSITIVO.
    #           Usa Field(gt=0, strict=True). ¿Por qué strict=True? Para que un
    #           string como "32" NO se convierta solo a int: queremos un int real.
    batch_size: int = Field(gt=0, strict=True)

    # device ya está resuelto como ejemplo de Literal (solo acepta estos valores).
    device: Literal["cpu", "cuda", "mps"] = "cpu"

    # --- Validadores: reglas que necesitan código ---

    # TODO (3): completa el validador de model_name.
    #   - mode no hace falta aquí (validamos el valor ya tipado como str).
    #   - Quita espacios con .strip().
    #   - Si queda vacío tras el strip, lanza ValueError("...").
    #   - Devuelve el valor limpio.
    @field_validator("model_name")
    @classmethod
    def require_nonblank_model_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("model_name no puede estar vacío ni ser solo espacios")
        return value

    # TODO (4): validador "before" para batch_size que rechace booleanos.
    #   En Python True == 1, así que un bool pasaría como entero sin este guardia.
    #   Reutiliza la idea de reject_boolean_threshold / reject_boolean_score.
    @field_validator("batch_size", mode="before")
    @classmethod
    def reject_boolean_batch_size(cls, value: object) -> object:
        if isinstance(value, bool):
            raise ValueError("batch_size no puede ser un booleano")
        return value


def load_settings(path: Path) -> Settings:
    """Lee el archivo JSON de configuración y lo valida con el modelo Settings.

    Args:
        path: ruta a config.json.

    Returns:
        Una instancia de Settings ya validada.

    Lanza:
        FileNotFoundError si el archivo no existe.
        pydantic.ValidationError si el contenido no cumple el contrato.
    """
    # TODO (5):
    #   1. Lee el texto del archivo: path.read_text(encoding="utf-8").
    #   2. Conviértelo a dict con json.loads(...).
    #   3. Valida y devuelve: Settings.model_validate(ese_dict).
    read = path.read_text(encoding="utf-8")
    data = json.loads(read)
    return Settings.model_validate(data)