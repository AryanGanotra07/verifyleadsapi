from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

@app.route("/")
def home():
    return "Verify Leads Api"


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")