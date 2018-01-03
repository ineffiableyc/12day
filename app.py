from flask import Flask, render_template, request, redirect,session
import requests, json
import urllib2
import simplejson as json
import pandas as pd
import bokeh
from bokeh.plotting import figure
from bokeh.embed import components


#app_lulu.vars={}
app = Flask(__name__)


#print (test)

#json_object = r.json


#print(json_object)
@app.route('/main')
#def main():
#  return redirect('/index')

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/graph',methods=['POST'])
def graph():

  ticker= request.form['ticker']


  url = "https://www.quandl.com/api/v3/datasets/WIKI/%s/data.json?api_key=sZHH2h365tvNXxTvQzMu" % ticker
  #api_key = 'sZHH2h365tvNXxTvQzMu'



  r = requests.get(url).json()
  #df= pd.DataFrame({col: dict(vals) for col, vals in r.items()})
  # json_object=json.loads(r)
  #test = r['datatable']
  df=pd.DataFrame(r['dataset_data']['data'], columns=r['dataset_data']['column_names'])
  df['Date'] = pd.to_datetime(df['Date'])


  df = df[['Date','Open' ,'Adj. Open', 'Close', 'Adj. Close']]


  plot = figure(title='Stock prices for %s' %ticker,
             x_axis_label='date',
             x_axis_type='datetime')

  print(request.form)
  if request.form.get('open'):
    plot.line(x=df['Date'].values, y=df['Open'].values, line_width=2, line_color="red", legend='Open')
  if request.form.get('adj_open'):
    plot.line(x=df['Date'].values, y=df['Adj. Open'].values, line_width=2, line_color="purple", legend='Adj. Open')
  if request.form.get('close'):
    plot.line(x=df['Date'].values, y=df['Close'].values, line_width=2, line_color="blue", legend='Close')
  if request.form.get('adj_close'):
    plot.line(x=df['Date'].values, y=df['Adj. Close'].values, line_width=2, line_color="green", legend='Adj. Close')
  script, div = components(plot)
  return render_template('graph.html', script=script, div=div)


if __name__ == '__main__':
  app.run(port=33507)