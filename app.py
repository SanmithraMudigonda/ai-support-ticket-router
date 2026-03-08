from fastapi import FastAPI
from pydantic import BaseModel
from router import classify_ticket

# Initialize FastAPI app
app = FastAPI()

# Define request schema
class Ticket(BaseModel):
    message: str

# API endpoint
@app.post("/route-ticket")
def route_ticket(ticket: Ticket):

    result = classify_ticket(ticket.message)

    return {
        "routing_result": result
    }