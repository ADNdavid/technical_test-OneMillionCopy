from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator
from datetime import datetime
import uuid

class LeadBase(SQLModel):
    nombre: str = Field(description="Nombre completo del usuario")
    email: str = Field(unique=True, description="Correo electrónico del usuario")
    telefono: Optional[str] = Field(default=None, description="Número de teléfono del usuario")
    fuente: str = Field(description="Fuente de donde proviene el lead")
    producto_interes: Optional[str] = Field(default=None, description="Producto de interés del usuario")
    presupuesto: Optional[float] = Field(default=None, description="Presupuesto en USD")
    
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

class Lead(LeadBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now, description="Fecha de registro en el sistema")
    updated_at: datetime = Field(default_factory=datetime.now, description="Fecha de última actualización del registro")
    deleted: bool = Field(default=False)

#class LeadCreate(Lead):
