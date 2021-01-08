#!/usr/bin/env python
from flask import Flask, request, make_response, jsonify
from model import TranslatorModel

server = Flask(__name__)

model = None


@server.route('/reload', methods = ['GET'])
def reload():
  global model
  lang = request.args.get('lang', default = None, type = str)
  if not lang:
    return make_response('', 200)
  
  model = TranslatorModel(lang)
  return make_response('', 200)


@server.route('/', methods = ['GET', 'POST'])
def translate():
  global model
  text = request.args.get('text', default = None, type = str) or request.form.get('text') 
  if not text:
    return make_response('', 200)
  if not model:
    return make_response('No trained model found / training may be in progress...', 200)

  t = model.translate(text)
  return make_response(t, 200)



if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=False)
