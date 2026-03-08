import re
from fastapi import FastAPI
from models import ExtractRequest, ExtractResponse, Entity

app = FastAPI(title="Text Extraction API")


def detect_entities(text: str):
    entities = []

    # Detect simple dates
    dates = re.findall(r"\d{1,2} de \w+( de \d{4})?", text)
    for d in dates:
        entities.append(Entity(name=d, type="DATE"))

    # Detect possible person names (very simple rule)
    persons = re.findall(r"[A-ZÁÉÍÓÚ][a-záéíóú]+ [A-ZÁÉÍÓÚ][a-záéíóú]+", text)
    for p in persons:
        entities.append(Entity(name=p, type="PERSON"))

    # Detect simple organizations
    if "Universidad" in text:
        entities.append(Entity(name="Universidad", type="ORG"))

    return entities


def detect_actions(text: str):
    actions = []

    if "confirmar" in text.lower():
        actions.append("Confirmar asistencia")

    if "coordinar" in text.lower():
        actions.append("Coordinar el evento")

    if "revisar" in text.lower():
        actions.append("Revisar el proyecto")

    return actions


def generate_summary(text: str):
    words = text.split()
    summary = " ".join(words[:40])
    return summary


def needs_clarification(text: str):
    if "próxima semana" in text.lower():
        return True
    if "decidir" in text.lower():
        return True
    return False


@app.post("/extract", response_model=ExtractResponse)
async def extract(req: ExtractRequest):

    text = req.text

    entities = detect_entities(text)
    actions = detect_actions(text)
    summary = generate_summary(text)

    clarification = needs_clarification(text)

    questions = []
    confidence = 0.8

    if clarification:
        confidence = 0.4
        questions = [
            "¿Cuál es la fecha exacta del evento?",
            "¿Dónde se realizará la reunión?",
            "¿Quién será responsable de la presentación?"
        ]

    return ExtractResponse(
        summary=summary,
        entities=entities,
        actions=actions if not clarification else [],
        confidence=confidence,
        needs_clarification=clarification,
        clarifying_questions=questions
    )


@app.get("/")
def root():
    return {"message": "Text Extraction API running"}
