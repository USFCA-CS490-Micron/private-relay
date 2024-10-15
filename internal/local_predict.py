import os

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
current_directory = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_directory, "../training/model-builds/hybrid-determination")
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
labels = ['offline_question', 'basic_question', 'complex_question', 'vision', 'explicit']
# offline_question      A query that can be answered by a lightweight local LLM (Language Model).
# basic_question   A query similar to a Google search, not requiring advanced reasoning, but needs up-to-date information.
# complex_question  A query that requires advanced reasoning or language analysis.
# vision    A query that requires visual processing.
# explicit  An inappropriate query that should be immediately discarded to avoid wasting processing power.



def predict(query: str):
    inputs = tokenizer(query, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_label = torch.argmax(logits, dim=-1).item()
    predicted_label_str = labels[predicted_label]
    return predicted_label_str





































