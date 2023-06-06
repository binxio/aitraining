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
    lander = """<!DOCTYPE html>
<html class="min-h-screen" lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" type="image/png" sizes="32x32" href="https://storage.googleapis.com/whatthepug/favicon.ico" />
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
    <link media="all" href="https://storage.googleapis.com/whatthepug/style.css" rel="stylesheet" />
    <title>What the Pug! The smartest and cutest models lending you a helping paw with all your language needs.</title>
    <meta name="description" content="What the Pug are online AI-powered models with the ability to help you with language" />
    <script src='https://storage.googleapis.com/whatthepug/textdiff.js'></script>
    <link rel="canonical" href="https://whatthepug.com/" />
  </head>
  <body class="body-wave overflow-x-hidden">
    <div class="overlay"></div>
    <div class="spinner">
      <div class="lds-grid"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <hr />
      Sniffing...
    </div>
    <header class="site-header-nav flex items-center nav-dark">
      <!-- nav -->
      <div class="absolute pin-t pin-l w-full z-40 nav-top">
        <nav class="px-4 md:px-8 flex justify-between items-center fade-down-load" class="primary" role="navigation" aria-label="Main Navigation">
          <div class="flex items-center">
            <a href="https://whatthepug.com">
              <img src='https://storage.googleapis.com/whatthepug/whatthepuglogo.png' />
            </a>
            <div class="menu-menu-eu-container">
              <ul id="menu-menu-eu" class="mt-2 ml-sm list-reset flex items-center nav-main relative">
                <li id="menu-item-1982" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-1982">
                  <a href="https://whatthepug.com/" aria-haspopup="true" aria-expanded="false">Home</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </div>
    </header>

    <section class="header-hero-main header-hero header-photo bg-purple md:flex overflow-hidden pb-md md:pb-0 relative header-home">
      <div class="h-overlay overlay-shade"></div>
      <div class="h-overlay overlay-gradient"></div>
      <div class="container pt-sm md:pt-0 pb-sm flex items-center px-6 md:px-0 relative z-20">
        <div class="w-full max-w-4xl pt-lg md:pr-md md:pt-0 pl-2 h-delay">
          <h1 class="text-white">What The Pug &#128062;</h1>
          <span class="subtitle text-white font-semibold text-base md:text-xl pb-4 block">Lending you a helping paw with language</span>
          <p class="text-lg md:text-2xl text-white pt-2 max-w-xl"></p>
          <label for="model-selector">Select Pug:</label>
          <select id="model-selector" name="model" onchange="showDiv(this)">
            <option value="--">--</option>
            <option value="1">Spelling Pug</option>
            <option value="2">Explainer Pug</option>
            <option value="3">Sentiment Pug</option>
          </select>
          <br />
          <br />
          <span style='color: #ccc;' class='introduction'>
            <p>Welcome to WhatThePug, your friendly, AI-powered linguistic sidekick! Created by <a href='https://linkedin.com/in/drvink/' target="_new" style='text-decoration: underline;'>Dennis Vink</a>, an esteemed AI Cloud Consultant at <a href='https://xebia.com/' target="_new" style='text-decoration: underline;'>Xebia</a>. The purpose of this website is to aid you in overcoming language hurdles you might encounter, ultimately elevating your language skills. My models are here to help with everything from spelling checks to comprehensive language explanations. They are eager to lend you a helping paw, ensuring language is both fun and effective.</p>
            <p>Meet my stellar trio: the Spelling Pug, the Explainer Pug, and the Sentiment Pug. Each has a unique specialized skill set to help you with your language needs. The Spelling Pug fixes style and grammar errors and shows you where your text differs from its suggestions. The Explainer Pug provides the gist of texts and signifies what the main points are. Lastly, the Sentiment Pug is skilled in discerning emotional undertones in language, enhancing your understanding of nuances in communication.</p>
          </span>
          <br />
          <div class="model">
            <table>
              <tr>
                <td>
                  <img class="modelimg" src="https://storage.googleapis.com/whatthepug/whatthepug-300x300_1.png" />
                </td>
                <td>
                  <textarea class="modelquestion" id='question' placeholder="Write your text here. Trust in the power of the model!" rows=8 cols=70></textarea>
                  <br />
                  <span class='style'>Style: <input type="radio" name="style" id='style' value="likethis" checked="">Unmodified <input type="radio" name="style" id='style' value="business">Business <input type="radio" name="style" id='style' value="informal">Informal <input type="radio" name="style" id='style' value="neutral">Neutral <input type="radio" name="style" id='style' value="friendly">Friendly</span>
                  <button class="modelbtn" id='ask'>Help me modelgie!</button> <span style='color: #ccc'>&#11013; &#65039; Click there for model help!</span>
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
          </div>
        </div>
      </div>
    </section>
    <script defer>
      const contentBlocks = document.querySelectorAll(".data-appear");
            const contentImgs = document.querySelectorAll(".data-img-zoom");
            const contentBlockGroup = document.querySelectorAll(".data-appear-group");
            const contentBlockGroupSm = document.querySelectorAll(".data-appear-group-sm");
            const header = document.querySelector(".header-hero-main");
            const blockOptions = {
              threshold: 0.1
            };
            const observer = new IntersectionObserver((entries, observer) => {
              entries.forEach(entry => {
                if (entry.isIntersecting) {
                  entry.target.classList.add('is-appeared');
                } else {
                  // entry.target.classList.remove('is-appeared');
                }
              });
            }, blockOptions);
            // Looping through the bars and adding them as targets of the observer
            Array.prototype.forEach.call(contentBlocks, (el) => {
              observer.observe(el);
            });
            Array.prototype.forEach.call(contentBlockGroup, (el) => {
              observer.observe(el);
            });
            Array.prototype.forEach.call(contentBlockGroupSm, (el) => {
              observer.observe(el);
            });
            Array.prototype.forEach.call(contentImgs, (el) => {
              observer.observe(el);
            });
            //Header load
            const headerObserver = new IntersectionObserver(function(entries, headerObserver) {
              entries.forEach(entry => {
                if (entry.isIntersecting) {
                  document.body.classList.add("header-is-on");
                  // observer.unobserve(entry.target);
                }
              });
            });
            headerObserver.observe(header);
    </script>
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
        var modelquestion = document.getElementById('question');
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
            modelquestion.placeholder = 'Write your text here, and select your preferred style. Spelling Pug will fix your spelling, style and grammar errors and rewrite your text in your preferred style. Trust in the power of the model!';
          } else {
            stylebox.style.display = 'none';
            difference.style.display = 'none';
            if(selectedValue == '2') {
              modelquestion.placeholder = 'Write your text here. Explainer Pug will summarise the key points and the intention of the author in plain English. Trust in the power of the model!';
            } else {
              modelquestion.placeholder = 'Write your text here. Sentiment Pug will tell you whether this is OK to send in a business context, and will tell you what the tone and sentiment of the message is. Trust in the power of the model!';
            }
          }
          let modelimg = document.querySelector('.modelimg');
          modelimg.src = 'https://storage.googleapis.com/whatthepug/whatthepug-300x300_' + selectedValue + '.png';
          modelDiv.style.display = 'block';
        }
      }

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
    </script>
    <script>
      document.getElementById('ask').addEventListener('click', async () => {
        const question = document.getElementById('question').value;
        const person = document.getElementById('model-selector').value;
        var styles = document.getElementsByName('style');
        var selectedStyle = 'none';

        for(var i = 0; i < styles.length; i++) {
            if(styles[i].checked){
                selectedStyle = styles[i].value;
                break;
            }
        }

        const answerTextarea = document.getElementById('answer');
        if (question.trim() === '') {
          alert('Please type a question.');
          return;
        }

        showSpinner();
        let response = await fetch('https://whatthepug.com/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ "question": question, "role": person, "style": selectedStyle }),
        });
        if (response.ok) {
          const data = await response.json();
          answerTextarea.value = data.answer.trim();
          var styles = document.getElementsByName('style');
          var selector = document.getElementById('model-selector');
          var selectedValue = selector.value;
          if(selectedValue == '1') {
            var wikEdDiff = new WikEdDiff();
            var orig = document.getElementById('question').value;
            var _new = data.answer.trim();
            var diffHtml = wikEdDiff.diff(orig, _new);
            var div = document.getElementById('diff');
            div.innerHTML = diffHtml;
          }
          hideSpinner();
        } else {
          answerTextarea.value = 'I am sleeping right now. Please try again later.';
          hideSpinner();
        }
      });
    </script>
    <script>
      function preselectOptionFromUrl() {
        const fragment = window.location.hash.substring(1);
        const selector = document.getElementById('model-selector');
        const menu = document.getElementById('menu-menu-eu');

        if (fragment && selector) {
          selector.value = fragment;
        }

        if (selector && menu) {
          menu.innerHTML='<li id="menu-item-1982" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-1982"><a href="https://whatthepug.com/" aria-haspopup="true" aria-expanded="false">Home</a></li>';
          for (let i = 0; i < selector.options.length; i++) {
            const option = selector.options[i];
            if (option.value !== '--' && option.value !== 'custom') {
              showDiv(selector);
              const li = document.createElement('li');
              li.classList.add('menu-item', 'menu-item-type-post_type', 'menu-item-object-page', 'menu-item-has-children');
              li.id = `menu-item-${i + 1000}`;

              const a = document.createElement('a');
              a.href = `#${option.value}`;
              a.setAttribute('aria-haspopup', 'true');
              a.setAttribute('aria-expanded', 'false');
              a.textContent = option.text;
              li.appendChild(a);
              menu.appendChild(li);
            }
          }
        }
      }
      document.addEventListener('DOMContentLoaded', preselectOptionFromUrl);
      window.addEventListener('hashchange', preselectOptionFromUrl);
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

