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


app = Flask(__name__)

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

# Lander HTML code is from WhatThePug.com. You'll want to replace it with something simpler I guess :)
@app.route('/', methods=['GET', 'POST'])
def landing_page():
    lander = """
<!DOCTYPE html>
<html class="min-h-screen" lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My AI Website</title>
    <meta name="description" content="My Amazing AI Tool" />
    <meta name="robots" content="noindex,nofollow">
  </head>
  <body>
    <textarea class="modelprompt" id='prompt' placeholder="Context and prompt" rows=8 cols=70></textarea>
    <br />
    <button class="modelbtn" id='ask'>Asketh</button> <span style='color: #ccc'>&#11013; &#65039; Click here to query!</span>
    <br />
    <br />
    </td>
    </tr>
    </table>
    <table>
      <tr>
        <td colspan=2>
          <textarea class="modelanswer" id='answer' placeholder="The model's answer will appear here..." rows=8 cols=101 readonly></textarea>
          <button id="copy-button">Copy answer</button>
        </td>
      </tr>
    </table>
    <table class='difference'>
      <div id='diff'></div>
    </table>
    <script type="text/javascript">
      function constructQueryString() {
        let name = encodeURIComponent(document.getElementById('name').value);
        let job = encodeURIComponent(document.getElementById('authority').value);
        let speaker = encodeURIComponent(document.getElementById('speaker').value);
        let context = encodeURIComponent(document.getElementById('context').value);
        let queryString = `https://whatthepug.com/?name=${name}&job=${job}&speaker=${speaker}&context=${context}`;
        console.log('Your AI URL:', queryString);
      }

      function createLabelAndElement(labelText, element, elementName) {
        const label = document.createElement('label');
        label.setAttribute('for', elementName);
        label.textContent = labelText + ': ';

        element.setAttribute('name', elementName);

        const container = document.createElement('span');
        container.appendChild(label);
        container.appendChild(element);

        return container;
      }

      function showDiv(elem) {
        var selectedValue = elem.value;
        var modelDiv = document.querySelector('.model');
        var intro = document.querySelector('.introduction');
        var modelprompt = document.getElementById('prompt');
        if (selectedValue === '--') {
          modelDiv.style.display = 'none';
          intro.style.display = 'block';
        } else {
          intro.style.display = 'none';
          let stylebox = document.querySelector('.style');
          let difference = document.querySelector('.difference');
          if(selectedValue == '1') {
            stylebox.style.display = 'block';
            difference.style.display = 'block';
            modelprompt.placeholder = 'Write your text here, and select your preferred style. Spelling Pug will fix your spelling, style and grammar errors and rewrite your text in your preferred style. Trust in the power of the model!';
          } else {
            stylebox.style.display = 'none';
            difference.style.display = 'none';
            if(selectedValue == '2') {
              modelprompt.placeholder = 'Write your text here. Explainer Pug will summarise the key points and the intention of the author in plain English. Trust in the power of the model!';
            } else {
              modelprompt.placeholder = 'Write your text here. Sentiment Pug will tell you whether this is OK to send in a business context, and will tell you what the tone and sentiment of the message is. Trust in the power of the model!';
            }
          }
          let modelimg = document.querySelector('.modelimg');
          modelimg.src = 'https://storage.googleapis.com/whatthepug/whatthepug-300x300_' + selectedValue + '.png';
          modelDiv.style.display = 'block';
        }
      }

    </script>
    <script>
      document.getElementById('ask').addEventListener('click', async () => {
        const prompt = document.getElementById('prompt').value;

        const answerTextarea = document.getElementById('answer');
        if (prompt.trim() === '') {
          alert('Please type a prompt.');
          return;
        }

        let response = await fetch('https://yourwebsiteurl.example.com/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ "prompt": prompt }),
        });
        if (response.ok) {
          const data = await response.json();
          answerTextarea.value = data.answer.trim();
          var styles = document.getElementsByName('style');
          var selector = document.getElementById('model-selector');
          var selectedValue = selector.value;
          if(selectedValue == '1') {
            var wikEdDiff = new WikEdDiff();
            var orig = document.getElementById('prompt').value;
            var _new = data.answer.trim();
            var diffHtml = wikEdDiff.diff(orig, _new);
            var div = document.getElementById('diff');
            div.innerHTML = diffHtml;
          }
        } else {
          answerTextarea.value = 'I am sleeping right now. Please try again later.';
        }
      });
    </script>
    <script>
      const copyButton = document.getElementById('copy-button');
      const textarea = document.getElementById('answer');
      copyButton.addEventListener('click', (event) => {
        textarea.select();document.execCommand('copy'); window.getSelection().removeAllRanges();
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

