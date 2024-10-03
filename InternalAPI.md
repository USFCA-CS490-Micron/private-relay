# internal api reference

## Vision
### `vision_query(query: str, subquery: str, image: image) -> str`
#### Takes a query string and image, returns analysis from service provider
`subquery` is occasionally generated on the core device by a local LLM if the user query is multistep.
A multistep query might be "How many calories are in this," which first requires
Google Cloud Vision be called with the subquery "what is this?" to identify the content(s),
then call Google Natural Language with `query + gcv_response` ("how many calories are in this" + "12 oz can of coca-cola")

If `subquery` is None, call `gc_vision(query, image)`, else call `gc_vision(subquery, image)`.

For ex (this won't work oob, and definitely wont work for things like OCR/doc reading if we want that):
```
vision_response = None
if subquery is not None:    # there *is* a subquery, so this is multistep
    vision_response = gc_vision(subquery, image) # "what is this" + img => "can of coca-cola"
    language_response = gc_language(query + vision_response) # query + vision_response == "How many calories are in this 12 oz can of coca-cola"
    return language_response
else if subquery is None:   # no subquery, only query
    return gc_vision(query, image) # might change this to also use gnl for summary
```


### ... keep going!