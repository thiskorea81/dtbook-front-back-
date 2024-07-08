from fastapi.responses import JSONResponse
from utils.openai_utils import generate_response

async def chat_with_student(prompt: dict):
    try:
        response = generate_response(prompt["prompt"])
        return JSONResponse(content={"response": response})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
