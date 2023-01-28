from flask import Flask, redirect, request
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)

@app.route('/gql')
def gql():
  headers = request.headers
  body = request.data
  res = requests.post("https://gql.twitch.tv/gql", headers=headers, body=body)
  return res.json()