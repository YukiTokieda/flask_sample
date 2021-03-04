from flask import Flask, render_template, request, session, url_for, redirect
from flask.views import MethodView
import random

import pickle

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  n = random.randrange(5,10)
  data = []
  for n in range(n):
    data.append(random.randrange(0,100))
  return render_template('index.html', title='Template Sample', message='これはサンプルのページです',data=data)

@app.route('/predict', methods=['GET','POST'])
def predict():
  if request.method == 'GET':
   msg = '販売価格を予想したい住宅情報を入力して下さい'
   return render_template('predict.html', title='Predict Page', message=msg)

  if request.method == 'POST':
    reg = pickle.load(open('./model/trained_model.pkl', 'rb'))
    x1 = request.form.get('tsubo')
    x2 = request.form.get('tsubo_su')
    x3 = request.form.get('kenpei')
    x4 = request.form.get('building')
    x5 = request.form.get('age')
    x6 = request.form.get('birth')
    area = request.form.get('area')

    if area == 'a':
      x7 = 1
      x8 = 0
      x9 = 0
    elif area == 'b':
      x7 = 0
      x8 = 1
      x9 = 0
    elif area == 'c':
      x7 = 0
      x8 = 0
      x9 = 1
    else :
      x7 = 0
      x8 = 0
      x9 = 0

    x = [[int(x1), float(x2), float(x3), int(x4), int(x5), int(x6), x7 ,x8 ,x9]]
    price = reg.predict(x)
    price = price[0][0]
    price = round(price, 2)

    price = 'この住宅の予想販売価格は：{}ドルです。'.format(price)
    return render_template('predict.html', title='Predict Page', message=price, tsubo=x1, tsubo_su=x2, kenpei=x3, building=x4, age=x5, birth=x6, area=area)

@app.route('/next', methods=['GET'])
def next():
  return render_template('next.html', title='Next Page', message='これは次のページのサンプルです', data=['A','B','C'])

@app.template_filter('sum')
def sum_filter(data):
  total = 0
  for item in data:
    total += item
  return total

app.jinja_env.filters['list_sum'] = sum_filter

@app.context_processor
def sample_processor():
  def total(n):
    total = 0
    for i in range(n + 1):
      total += i
    return total
  return dict( total = total )


app.secret_key = b'asdfghjkl'

class HelloAPI( MethodView ):
  send = ''
  def get(self):
    if 'send' in session:
      msg = 'send：' + session['send']
      send = session['send']

    else:
      msg = 'メッセージを書いてください'
      send = ''

    return render_template('next.html', title='Next Page', message=msg, send=send)

  def post(self):
    session['send'] = request.form['send']
    return redirect('/hello/')

app.add_url_rule('/hello/', view_func=HelloAPI.as_view('hello'))

if __name__ == '__main__':
  app.run(host='localhost', debug=True)

