import os
from openai import OpenAI
from google.cloud import vision
from google.cloud import language_v2

class QueryProcessor:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.vision_client = vision.ImageAnnotatorClient()
        self.language_client = language_v2.LanguageServiceClient()
        self.gpt_system_prompt = os.getenv('GPT_SYSTEM_PROMPT')
        if self.gpt_system_prompt is None:
            raise ValueError("GPT_SYSTEM_PROMPT must be set in .env file")

    def query_gpt(self, query: str, entities: str = None):
        if entities:
            enhanced_query = f"Given these identified entities: {entities}\n\nQuery: {query}"
        else:
            enhanced_query = query

        prompt = [
            {"role": "system", "content": self.gpt_system_prompt},
            {"role": "user", "content": enhanced_query}
        ]
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt,
            temperature=0.0,
        )
        
        return response.choices[0].message.content if response.choices else None

    def preprocess_with_gnl(self, query: str):
        document = {
            "content": query,
            "type_": language_v2.Document.Type.PLAIN_TEXT,
            "language_code": "en",
        }
        response = self.language_client.analyze_entities(
            request={"document": document, "encoding_type": language_v2.EncodingType.UTF8}
        )
        return ', '.join([f"{entity.name} ({language_v2.Entity.Type(entity.type_).name})" 
                         for entity in response.entities])

    def query_vision(self, query: str, image):
        try:
            vision_response = self.query_google_vision(image)
            language_response = self.preprocess_with_gnl(query)
            
            enhanced_query = f"""
            Image content: {vision_response}
            Identified entities: {language_response}
            User query: {query}
            """
            
            return self.query_gpt(enhanced_query)
        except Exception as e:
            print(f"Error in vision query processing: {str(e)}")
            raise

    def query_google_vision(self, image):
        content = image.read()
        image = vision.Image(content=content)
        response = self.vision_client.label_detection(image=image)
        labels = response.label_annotations
        return ', '.join([label.description for label in labels])