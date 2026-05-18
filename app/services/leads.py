import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from sqlmodel import Session, func, select
from ..models.leads import Lead
from datetime import datetime, timedelta


def _active_lead_query():
    return select(Lead).where(Lead.deleted == False)


def _apply_lead_filters(query, fuente=None, fecha_inicio=None, fecha_fin=None):
    if fuente:
        query = query.where(Lead.fuente == fuente)
    if fecha_inicio:
        query = query.where(Lead.created_at >= fecha_inicio)
    if fecha_fin:
        query = query.where(Lead.created_at <= fecha_fin)
    return query


def get_leads_stats(session: Session):
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)

    total_leads = session.exec(select(func.count(Lead.id)).select_from(Lead).where(Lead.deleted == False)).one()
    leads_por_fuente = session.exec(
        select(Lead.fuente, func.count(Lead.id)).where(Lead.deleted == False).group_by(Lead.fuente)
    ).all()
    avg_presupuesto = session.exec(
        select(func.avg(Lead.presupuesto)).where(Lead.deleted == False)
    ).one() or 0.0
    leads_ultimos_7_dias = session.exec(
        select(func.count(Lead.id)).where(Lead.deleted == False, Lead.created_at >= seven_days_ago)
    ).one()

    return {
        "total_leads": total_leads,
        "leads_por_fuente": dict(leads_por_fuente),
        "promedio_presupuesto": float(round(avg_presupuesto, 2)),
        "leads_ultimos_7_dias": leads_ultimos_7_dias,
    }


def _serialize_lead(lead: Lead) -> dict:
    return {
        "id": lead.id,
        "nombre": lead.nombre,
        "email": lead.email,
        "telefono": lead.telefono,
        "fuente": lead.fuente,
        "producto_interes": lead.producto_interes,
        "presupuesto": lead.presupuesto,
    }


def get_leads_ai_summary(
    session: Session,
    fuente: str | None = None,
    fecha_inicio: datetime | None = None,
    fecha_fin: datetime | None = None,
) -> str:
    query = _apply_lead_filters(_active_lead_query(), fuente, fecha_inicio, fecha_fin)
    leads = session.exec(query).all()
    if not leads:
        return "No se encontraron leads que coincidan con los filtros especificados."

    prompt = _build_summary_prompt(
        [_serialize_lead(lead) for lead in leads], fuente, fecha_inicio, fecha_fin
    )
    return _call_openai(prompt)


def _build_summary_prompt(leads_data, fuente, fecha_inicio, fecha_fin) -> str:
    filters = [
        f"Fuente: {fuente}" if fuente else None,
        f"Fecha inicio: {fecha_inicio.isoformat()}" if fecha_inicio else None,
        f"Fecha fin: {fecha_fin.isoformat()}" if fecha_fin else None,
    ]
    filter_text = ", ".join([item for item in filters if item]) or "Sin filtros"

    return (
        "Eres un analista de leads. Recibes la siguiente lista de leads y debes generar un resumen ejecutivo. "
        "El resumen debe incluir: análisis general, fuente principal y recomendaciones.\n\n"
        f"Filtros aplicados: {filter_text}.\n\n"
        f"Leads:\n{json.dumps(leads_data, ensure_ascii=False, indent=2)}\n\n"
        "Genera el resumen ejecutivo en un solo texto corto y claro."
    )


def _call_openai(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no está configurada en el entorno")

    url = "https://api.openai.com/v1/chat/completions"
    payload = json.dumps(
        {
            "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            "messages": [
                {"role": "system", "content": "Eres un asistente útil para análisis de leads."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 500,
        }
    ).encode("utf-8")

    request = Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=30) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Error llamando a OpenAI: {exc.code} {exc.read().decode('utf-8')}" )
    except URLError as exc:
        raise RuntimeError(f"Error de red al llamar a OpenAI: {exc.reason}")

    message = response_data.get("choices", [{}])[0].get("message", {}).get("content")
    if not message:
        raise RuntimeError("Respuesta de OpenAI incompleta o vacía")

    return message.strip()
