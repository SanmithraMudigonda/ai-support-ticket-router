from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_ticket(message: str):
    """
    Classifies a support ticket into department, priority, and summary.
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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    # Remove markdown code blocks if present
    content = content.replace("```json", "").replace("```", "").strip()

    return json.loads(content)