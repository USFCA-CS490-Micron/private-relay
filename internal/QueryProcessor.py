import requests

class QueryProcessor:

    # TODO  this should call google vision to get text response for content of image,
    #       form a query based on response to send to google language
    #       for example:
    #       "How many calories are in this?" (image = can of coke)
    #       -> send image
    #       -> send query to a local model (it will figure out what's important and query-worthy)
    #       -> send local model's response to google language
    def query_vision(self, query, image):
        pass

    # TODO  this is separate because it would be nice to be able to switch providers based on relevance
    #       for ex, if one provider is better at a task than another, we could use a switch in query_vision()
    def query_google_vision(self, image):
        pass

    # TODO  System prompt will come from cognition if necessary
    def query_google_language(self, query: str):
        pass

    # TODO  We'll use the GPT-4o mini model, system prompt will come from cognition work
    def query_gpt(self, query: str):
        pass