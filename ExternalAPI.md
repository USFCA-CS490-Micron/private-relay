# external api reference


## Vision


#### Vision Query:
Takes a query string and image, returns analysis.

##### Request
```
{
    type: 'vision',
    query: str,
    media: image
}
```
call `vision_query(query: str, image: image) -> str`, return to client:

##### Response
```
# We'll need to add more
    {
        response: str
    }
```

### `gc_vision(query: str, image: image) -> str`
#### Gets a description from Google Cloud Vision
Sends the query and image to Google Cloud Vision, return analysis

*have to figure out how the GCV calls are structured, read their docs*

## Language

### `gc_language(query) -> str`
Queries Google Natural Language for `vision_query()` and `basic_question` external API calls

### `gpt_mini(query) -> str`
Queries GPT-4o mini for `complex_question` external API calls.

### and more...




