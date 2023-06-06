import os
import vertexai
from vertexai.preview.language_models import TextGenerationModel

from flask import Flask

app = Flask(__name__)

def predict_large_language_model_sample(
    project_id: str,
    model_name: str,
    temperature: float,
    max_decode_steps: int,
    top_p: float,
    top_k: int,
    content: str,
    location: str = "us-central1",
    tuned_model_name: str = "",
    ) :
    """Predict using a Large Language Model."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    if tuned_model_name:
      model = model.get_tuned_model(tuned_model_name)
    response = model.predict(
        content,
        temperature=temperature,
        max_output_tokens=max_decode_steps,
        top_k=top_k,
        top_p=top_p,)
    return(response.text)


@app.route('/')
def hello_world():
    return(predict_large_language_model_sample("playground-dennisvink", "text-bison@001", 0.7, 1024, 1.0, 40, "Create a rhyme", "us-central1"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

