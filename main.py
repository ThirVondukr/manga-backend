"""
Main file for development purposes
"""
import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(".env")
    uvicorn.run(app="app:create_app", factory=True, reload=True, host="0.0.0.0")
