import os
import requests
from openai import OpenAI
from google.cloud import vision
from google.cloud import language_v2



class QueryProcessor:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.vision_client = vision.ImageAnnotatorClient()
        self.language_client = language_v2.LanguageServiceClient()
        self.gpt_system_prompt = os.getenv("GPT_SYSTEM_PROMPT")

    # TODO  this should call google vision to get text response for content of image,
    #       form a query based on response to send to google language
    #       for example:
    #       "How many calories are in this?" (image = can of coke)
    #       -> send image
    #       -> send query to a local model (it will figure out what's important and query-worthy)
    #       -> send local model's response to google language
    def query_vision(self, query, image):
        vision_response = self.query_google_vision(image)
        language_response = self.query_google_language(query)
        combined_response = f"""
                Image label information: {vision_response}
                Relevant entity information: {language_response}
                """
        query += combined_response
        response = self.query_gpt(query, self.gpt_system_prompt)
        return response

    # TODO  this is separate because it would be nice to be able to switch providers based on relevance
    #       for ex, if one provider is better at a task than another, we could use a switch in query_vision()
    def query_google_vision(self, image):
        content = image.read()
        image = vision.Image(content=content)
        response = self.vision_client.label_detection(image=image)
        labels = response.label_annotations
        vision_response = ', '.join([label.description for label in labels])
        return vision_response

    # TODO  System prompt will come from cognition if necessary
    def query_google_language(self, query: str):
        document = {
            "content": query,
            "type_": language_v2.Document.Type.PLAIN_TEXT,
            "language_code": "en",
        }
        response = self.language_client.analyze_entities(
            request={"document": document, "encoding_type": language_v2.EncodingType.UTF8}
        )
        result = ', '.join([f"{entity.name} ({language_v2.Entity.Type(entity.type_).name})" for entity in response.entities])
        return result


    # TODO  We'll use the GPT-4o mini model, system prompt will come from cognition work
    def query_gpt(self, query: str, gpt_system_prompt: str):
        prompt = [
            {"role": "system", "content": gpt_system_prompt},
            {"role": "user", "content": query}
        ]
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt,
            temperature=0.0,
        )
        return response.choices[0].message.content if response.choices else None