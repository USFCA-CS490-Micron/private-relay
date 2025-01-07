import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from internal.query_processor import QueryProcessor
import uvicorn
import traceback
from dotenv import load_dotenv
import os
os.environ.clear()
load_dotenv()


class API:
    def __init__(self):
        self.qp = QueryProcessor()
        self.app = FastAPI()

        @self.app.post("/api/query")
        async def process_query(
            type: str,
            query: str,
        ):
            print(f"\nReceived request - Type: {type}, Query: {query}")
            
            try:
                if type == "complex":
                    result = self.gpt_mini(query)
                    print(f"Complex query result: {result}")
                    return result
                elif type == "vision":
                    raise HTTPException(
                        status_code=501, 
                        detail="Vision queries not yet implemented"
                    )
                else:
                    raise HTTPException(
                        status_code=400, 
                        detail="Only 'complex' and 'vision' query types are supported. Basic queries should be processed locally."
                    )
            except Exception as e:
                print(f"Error processing request: {str(e)}")
                print("Full traceback:")
                print(traceback.format_exc())
                raise HTTPException(status_code=500, detail=str(e))

    def gpt_mini(self, query: str):
        try:
            print(f"Processing GPT query: {query}")
            
            try:
                entities = self.qp.preprocess_with_gnl(query)
                print(f"GNL identified entities: {entities}")
            except Exception as e:
                print(f"Warning: GNL processing failed: {str(e)}")
                entities = "No entities identified"
            
            try:
                result = self.qp.query_gpt(query, entities)
                print(f"GPT returned result: {result}")
                
                return {
                    "entities": entities,
                    "result": result
                }
            except Exception as e:
                print(f"Error in GPT processing: {str(e)}")
                print(traceback.format_exc())
                raise
                
        except Exception as e:
            print(f"Error in gpt_mini: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

api = API()

if __name__ == "__main__":
    print("\nStarting API server...")
    uvicorn.run(api.app, host="0.0.0.0", port=80)