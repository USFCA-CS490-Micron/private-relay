from fastapi import FastAPI, File, UploadFile
from typing import Optional
from ..internal import QueryProcessor
import io
from PIL import Image


qp = QueryProcessor.QueryProcessor()
app = FastAPI()


def gc_language(query: str):
    return qp.query_google_language(query)


def gpt_mini(query: str):
    return qp.query_gpt(query)


@app.post("/process-query")
async def process_query(
    type: str,
    query: str,
    media: Optional[UploadFile] = None
):
    if type == "basic":
        return gc_language(query)
    elif type == "complex":
        return gpt_mini(query)
    elif type == "vision":
        if media is not None:
            try:
                image_stream = io.BytesIO(await media.read())
                image = Image.open(image_stream)
            except Exception as e:
                return {'error': f'Invalid image file: {str(e)}'}

            try:
                result = qp.query_vision(query, image)
                return result
            except Exception as e:
                return {'error': f'Error processing image: {str(e)}'}
        else:
            return {"error": "Vision type requires an image file"}
    else:
        return {"error": "Invalid type specified"}