from dotenv import load_dotenv

load_dotenv(".env")

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app="app:create_app", factory=True, host="0.0.0.0", port=8000)
