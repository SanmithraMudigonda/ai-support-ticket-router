from fastapi import FastAPI
from pydantic import BaseModel, Field
from router import classify_ticket

# Initialize FastAPI app
app = FastAPI(title="AI Support Ticket Router")


# -----------------------------
# Request Schema
# -----------------------------
class Ticket(BaseModel):
    message: str = Field(..., min_length=10, max_length=1000)
    # input validation of message for FastAPI to avoid bad requests


# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/route-ticket")
def route_ticket(ticket: Ticket):

    result = classify_ticket(ticket.message)

    return {
        "routing_result": result
    }