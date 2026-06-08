# FastAPI server that accepts notes through a POST request,
# validates the request data, generates flashcards, and
# returns the results as a JSON response.

import uvicorn  
import time     
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# NOTE: you will implement this code
from flashcard_generator import generate_flashcards

# create the FastAPI app
app = FastAPI()

# Add CORS middleware so browsers can make requests to this API
# from any origin. Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
# and all request headers (Content-Type, Authorization, etc.).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# This middleware is used to find the time taken to process each request and adds it as a header in the response.
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request) # call_next passes the request to the next middleware or route handler and waits for the response
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# This is a pydantic model which defines the structure of the request body. It has two fields:
# - notes: a string and is required
# - cards: an integer and is optional with a default value of 3
class GenerateRequest(BaseModel):
    notes: str
    cards: int = 3



# This the post API endpoint which takes a GenerateRequest object as input , validates it against the GenerateRequest model, 
# and then calls the generate_flashcards function to generate flashcards based on the input notes and number of cards. 
# If there is any error during the process, it catches the exception and returns a 500 Internal Server Error with the error message.
@app.post("/api/generate")
async def generate_cards(request: GenerateRequest):
    try:
        result = await generate_flashcards(request.notes, request.cards)
        
        
        return result
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Server running on http://localhost:3000")
    #Uvicorn is a server that runs the FastAPI application. It listens on all available network interfaces and runs on port 3000. 
    uvicorn.run(app, host="0.0.0.0", port=3000)