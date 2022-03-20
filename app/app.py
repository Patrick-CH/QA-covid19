from QA_app.ChatBot import ChatBot
from forms import AskForm
from flask import Flask, redirect, abort, make_response, request, session, url_for, render_template, flash, Markup
import sys

sys.path.append("D:\workspace\PycharmProjects\Covid-19-QA\QA_app")

app = Flask(__name__)
app.secret_key = 'kbLBLH12BUYV12hv'
chatBot = ChatBot()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AskForm()
    if form.submit.data and form.validate():
        q = form.question.data
        ans = chatBot.answer(q)
        return render_template('index.html', form=form, ans=ans.split('\n'))
    return render_template('index.html', form=form)


@app.route('/chat', methods=['POST'])
def chat():
    form_data = request.form
    if form_data:
        q = form_data['question']
        ans = chatBot.answer(q)
        return {'ans': ans}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
