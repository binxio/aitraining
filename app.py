import base64
import json
import os
import urllib.parse
import urllib.request
import openai

from flask import Flask, request, jsonify

openai.api_key = os.environ.get('OPENAI_PROXY_API_KEY') # Configure this in Cloud Run
openai.api_base =  "https://ai.xebia.com/"
openai.api_type = 'azure'
openai.api_version = "2023-03-15-preview"


app = Flask(__name__, static_url_path='', static_folder='static')

def ask_model(context):
    prompt = f"""{context}"""
    response = openai.ChatCompletion.create(
        engine='gpt-4-us',
        messages=[
            {"role": "system", "content": f"You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message["content"]

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    lander = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>Xebia Sample AI Tool</title>
    <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/css/Nunito.css">
    <link rel="stylesheet" href="assets/css/aitool.css">
  </head>
  <body id="page-top">
    <div class="overlay"></div>
    <div class="spinner">
      <div class="lds-grid"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <div class="text-center thinking"><span>Thinking...</span></div>
    </div>
    <div id="wrapper">
      <div class="d-flex flex-column" id="content-wrapper">
        <div id="content">
          <div class="container-fluid">
            <div class="d-sm-flex justify-content-between align-items-center mb-4">
              <h3 class="text-dark mb-0"></h3>
            </div>
            <section class="py-4 py-xl-5">
              <div class="card mb-5">
                <div class="card-body p-sm-5">
                  <h2 class="text-center mb-4">Xebia AI Tool</h2>
                  <div class="mb-3">
                    <textarea class="form-control" id="input" name="message" rows="8" placeholder="Input to LLM"></textarea>
                    <br />
                    <textarea class="form-control" id="output" name="message" rows="8" placeholder="Output of LLM"></textarea>
                  </div>
                  <div><button class="btn btn-primary d-block w-100 querybtn" id='querybtn' type="submit">Query LLM</button></div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
    <script src="assets/bootstrap/js/bootstrap.min.js"></script>
    <script src="assets/js/theme.js"></script>
    <script>
      function showSpinner() {
        var overlay = document.querySelector('.overlay');
        var spinner = document.querySelector('.spinner');

        overlay.style.display = 'block';
        spinner.style.display = 'block';
      }

      function hideSpinner() {
        var overlay = document.querySelector('.overlay');
        var spinner = document.querySelector('.spinner');

        overlay.style.display = 'none';
        spinner.style.display = 'none';
      }

      document.getElementById('querybtn').addEventListener('click', async () => {
        const prompt = document.getElementById('input').value;
        const answerTextarea = document.getElementById('output');
        if (prompt.trim() === '') {
          alert('Please type a prompt.');
          return;
        }
        showSpinner();
        let response = await fetch(window.location.origin + "/", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ "prompt": prompt }),
        });
        if (response.ok) {
          const data = await response.json();
          answerTextarea.value = data.answer.trim();
        } else {
          answerTextarea.value = 'I am sleeping right now. Please try again later.';
        }
        hideSpinner();
      });
    </script>
  </body>
</html>
"""
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data:
            prompt = post_data.get('prompt')
            return jsonify({'answer': ask_model(prompt)})
        else:
            return jsonify({"message": "No data received"}), 400
    else:
        return(lander)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

