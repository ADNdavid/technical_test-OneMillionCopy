from sqlmodel import SQLModel, Field, field_validator
from typing import Optional

class Lead(SQLModel, table=True):
    nombre: str 
    email: str = Field(unique=True)
    telefono: Optional[str] = Field(default=None)
    fuente: str
    producto_interes: Optional[str] = Field(default=None)
    presupuesto: Optional[float] = Field(default=None)
    
    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, value):
        if not value:
            raise ValueError('El nombre es requerido')
        if len(value) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return value
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, value):
        if '@' not in value:
            raise ValueError('El email debe contener un "@"')
        return value

    @field_validator('fuente')
    @classmethod
    def validar_fuente(cls, value):
        permitidos = ["instagram", "facebook", "landing_page", "referido", "otro"]
        if not value:
            raise ValueError('La fuente es requerida')
        if value not in permitidos:
            raise ValueError('La fuente no es válida, debe ser una de las siguientes: ' + ', '.join(permitidos))
        return value
