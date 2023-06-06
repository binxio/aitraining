import openai

openai.api_key = "SecretAPIKey"
openai.api_base =  "https://ai.xebia.com/"
openai.api_type = 'azure'
openai.api_version = "2023-03-15-preview"

def query_gpt(context):
    prompt = f"""{context}"""
    response = openai.ChatCompletion.create(
        engine='gpt-4-us',
        messages=[
            {"role": "system", "content": f"You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message["content"]

print(query_gpt("Write a rhyme about the love child of Sinterklaas and Santa Claus. Write at least 15 lines in Dutch and use street language."))
