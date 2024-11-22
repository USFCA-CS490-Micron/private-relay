from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Optional
from internal.QueryProcessor import QueryProcessor
import io
from PIL import Image
import uvicorn

class InvalidImage(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class API:
    def __init__(self):
        self.qp = QueryProcessor()
        self.app = FastAPI()

        @self.app.post("/api/query")
        async def process_query(
            type: str,
            query: str,
            media: Optional[UploadFile] = None
        ):
            if type == "basic":
                return self.gc_language(query)
            elif type == "complex":
                return self.gpt_mini(query)
            elif type == "vision":
                if media is not None:
                    try:
                        image_stream = io.BytesIO(await media.read())
                        image = Image.open(image_stream)
                    except Exception as e:
                        raise InvalidImage(str(e))

                    try:
                        result = self.qp.query_vision(query, image)
                        return result
                    except Exception as e:
                        raise HTTPException(status_code=500, detail=str(e))
                else:
                    raise HTTPException(status_code=400, detail="Vision type requires an image file.")
            else:
                raise HTTPException(status_code=400, detail="Invalid type specified.")

    def gc_language(self, query: str):
        return self.qp.query_google_language(query)

    def gpt_mini(self, query: str):
        return self.qp.query_gpt(query)


api = API()

if __name__ == "__main__":
    uvicorn.run(api.app, host="0.0.0.0", port=80)