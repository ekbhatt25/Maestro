from groq import Groq

from app.config import settings

_client = Groq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """You are Maestro, an expert music practice coach.
You give specific, constructive feedback on a student's playing based on their audio features and relevant music theory.
Be encouraging but honest. Structure your feedback with:
1. What they did well
2. What to improve
3. A specific exercise to practice"""


def generate_feedback(transcript: str, features: dict, context: str) -> str:
    user_message = f"""
Music theory context:
{context}

Audio analysis:
- Tempo: {features.get('tempo_bpm')} BPM
- Pitch: {features.get('pitch_hz')} Hz
- Dynamics (RMS): {features.get('dynamic_rms')}

Transcript: {transcript or 'No vocals detected'}

Please provide feedback on this practice session.
"""
    response = _client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content
