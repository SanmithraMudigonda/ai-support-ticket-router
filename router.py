from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# Output Schema Validation
# -----------------------------
class RoutingDecision(BaseModel):
    department: str
    priority: str
    summary: str


# -----------------------------
# Fallback Routing
# -----------------------------
def fallback_route():
    """
    Returns a safe routing decision if the AI fails.
    """
    return {
        "department": "customer_support",
        "priority": "medium",
        "summary": "Fallback routing triggered due to classification failure."
    }


# -----------------------------
# JSON Cleanup
# -----------------------------
def clean_json(content: str):
    """
    Removes markdown formatting that LLMs sometimes include.
    """
    content = content.replace("```json", "")
    content = content.replace("```", "")
    return content.strip()


# -----------------------------
# Ticket Classification
# -----------------------------
def classify_ticket(message: str):
    """
    Classifies a support ticket into department, priority, and summary
    using an LLM. Includes structured output validation and fallback routing.
    """

    prompt = f"""
You are an AI support automation system.

Analyze the customer support message and return JSON with:
department
priority
summary

Departments:
- billing
- customer_support
- logistics
- technical_support

Priorities:
- low
- medium
- high

Customer message:
{message}

Return ONLY valid JSON.
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content

        # Clean markdown
        content = clean_json(content)

        # Convert JSON string → Python dictionary
        data = json.loads(content)

        # Validate structure using schema
        validated = RoutingDecision(**data)

        return validated.dict()

    except Exception:
        # If anything fails (LLM, JSON parsing, validation)
        return fallback_route()