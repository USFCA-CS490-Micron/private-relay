import requests
from openai import OpenAI

# pip install google-cloud-vision
from google.cloud import vision
# pip install --upgrade google-cloud-language
from google.cloud import language_v2
from local_predict import predict
from local_llm import local_llm_predict


# query_google_vision calls the Google Cloud Vision API to recognize image information. API setup details: https://cloud.google.com/vision/docs/setup?hl=zh-cn
# query_google_language calls the Google Natural Language API to recognize entities in the query. Specific details can be found in the following link: https://www.cloudskillsboost.google/focuses/582?catalog_rank=%7B%22rank%22:1,%22num_filters%22:0,%22has_search%22:true%7D&parent=catalog&search_id=31485341?utm_source=cgc-site&utm_medium=et&utm_campaign=FY24-Q2-global-website-skillsboost&utm_content=developers&utm_term=-
# Combine the results of these two into a string, which will become the content of the system prompt (basically saying that I have some image information (vision_response), and some entity information from the query (language_response), and the model needs to return a response based on this information).



def system_message(message: str) -> any:
    return {"role": "system", "content": message}


def user_message(message: str) -> any:
    return {"role": "user", "content": message}


def assistant_message(message: str) -> any:
    return {"role": "assistant", "content": message}


def submit_prompt(prompt) -> str:
    # api key
    openai_client = OpenAI(api_key='')

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt,
        stop=None,
        temperature=0.7,
    )

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content


class QueryProcessor:

    # TODO  this should call google vision to get text response for content of image,
    #       form a query based on response to send to google language
    #       for example:
    #       "How many calories are in this?" (image = can of coke)
    #       -> send image
    #       -> send query to a local model (it will figure out what's important and query-worthy)
    #       -> send local model's response to google language
    def query_vision(self, query, image):
        query_label = predict(query)
        if query_label == "offline_question":
            return local_llm_predict(query)
        elif query_label == "basic_question":
            pass
        elif query_label == "complex_question":
            language_response = self.query_google_language(query)
            system_prompt = f"""
            You will answer my question based on the following information:

            1. Relevant entity information extracted from the question (language_response): {language_response}

            Please synthesize the above information and accurately respond to my query. If you are uncertain about any aspects, please indicate the reasons for your uncertainty and make reasonable inferences based on the available information.
            """
            response = self.query_gpt(query, system_prompt)
            return response
        elif query_label == "vision":
            vision_response = self.query_google_vision(image)
            language_response = self.query_google_language(query)
            system_prompt = f"""
    You will answer my question based on the following information:
    
    1. Image label information (vision_response): {vision_response}
    2. Relevant entity information extracted from the question (language_response): {language_response}
    
    Please synthesize the above information and accurately respond to my query. If you are uncertain about any aspects, please indicate the reasons for your uncertainty and make reasonable inferences based on the available information.
    """
            response = self.query_gpt(query, system_prompt)
            return response
        elif query_label == "explicit":
            return "A query which is inappropriate "

    # TODO  this is separate because it would be nice to be able to switch providers based on relevance
    #       for ex, if one provider is better at a task than another, we could use a switch in query_vision()
    def query_google_vision(self, image):
        # https://cloud.google.com/vision/docs/labels?hl=zh-cn#vision_label_detection-python
        # Link for label detection (for example, identifying 'Coca-Cola')
        client = vision.ImageAnnotatorClient()
        content = image.read()
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        vision_response = ', '.join([label.description for label in labels])
        return vision_response

    # TODO  System prompt will come from cognition if necessary
    def query_google_language(self, query: str):
        # https://cloud.google.com/natural-language/docs/samples/language-entities-text?hl=zh_cn#language_entities_text-python
        # Link for analyzing entities in a string (for example, returning information about 'Coca-Cola'). Not sure which Google Language API to use.
        client = language_v2.LanguageServiceClient()
        document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT
        language_code = "en"
        document = {
            "content": query,
            "type_": document_type_in_plain_text,
            "language_code": language_code,
        }
        encoding_type = language_v2.EncodingType.UTF8
        response = client.analyze_entities(
            request={"document": document, "encoding_type": encoding_type}
        )
        result = ""
        for entity in response.entities:
            result += f"{entity.name} ({language_v2.Entity.Type(entity.type_).name}), "
        language_response = result.rstrip(", ")
        return language_response

    # TODO  We'll use the GPT-4o mini model, system prompt will come from cognition work
    def query_gpt(self, query: str, system_prompt: str):
        response = submit_prompt([
            system_message(
                system_prompt
            ),
            user_message(query),
        ])
        return response