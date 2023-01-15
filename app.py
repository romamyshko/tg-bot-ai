from flask import Flask
from flask import request
from flask import Response
import requests
import openai

openai.api_key = "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"
TOKEN = "5421447790:AAFIwWjNKd0jpSjpsUsGJaFItsNipiHckmM"
app = Flask(__name__)
 
def parse_message(message):
    print("message-->",message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id,txt
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)
        chat_id,txt = parse_message(msg)

        if txt == "/start":
            tel_send_message(chat_id, 'Hello, It\'s AI bot from OpenAI. Please ask any question :)')

        question = txt

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{question}",
            max_tokens=1024,
            n = 1,
            stop=None,
            temperature=0.5
        )
        answer = response["choices"][0]["text"]
        tel_send_message(chat_id, answer)
       
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=4998)