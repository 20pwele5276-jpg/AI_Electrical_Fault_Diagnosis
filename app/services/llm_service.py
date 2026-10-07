import os

from dotenv import load_dotenv
from groq import Groq, NotFoundError, PermissionDeniedError


load_dotenv()


# "llama-3.1-8b-instant" was retired by Groq (Aug 16, 2026).
# Models are tried in order; set GROQ_MODEL in .env to choose the first one.
MODELS = [
    os.getenv("GROQ_MODEL") or "openai/gpt-oss-20b",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
]


def explain_fault(
    fault,
    voltage,
    current,
    frequency,
    power_factor,
    temperature,
):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "LLM explanation is unavailable because the API key is not configured."

    client = Groq(api_key=api_key)

    prompt = f"""
You are an electrical troubleshooting assistant.

A machine learning system detected this possible fault:

Fault: {fault}
Voltage: {voltage} V
Current: {current} A
Frequency: {frequency} Hz
Power Factor: {power_factor}
Temperature: {temperature} °C

Explain this result in very simple language for a non-technical person.

Give:
1. What this fault means
2. Why these readings may indicate it
3. What an electrical worker should check

Keep the explanation short and practical.

Do not claim that the fault is confirmed.
"""

    last_error = None

    # Remove duplicates but keep order
    for model in dict.fromkeys(MODELS):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.2,
            )

            return response.choices[0].message.content

        except (NotFoundError, PermissionDeniedError) as error:
            # Model retired or not available for this key: try the next one.
            last_error = error

    raise RuntimeError(
        f"No available Groq model could generate the explanation. Last error: {last_error}"
    )
