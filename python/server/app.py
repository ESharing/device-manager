from flask import Flask, request
import json
from netconf_fun import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/yang-schemas', methods = ['GET'])
def getNodeSchemas():
    ip = request.args.get('ip')
    ne_type = request.args.get('type')
    schema_data = getSchemas(ip,ne_type)

    return json.dumps(schema_data)

@app.route('/objects', methods = ['GET'])
def getNodeObjects():
    ip = request.args.get('ip')
    ne_type = request.args.get('type')
    mo_data = getObjects(ip,ne_type)

    return json.dumps(mo_data)

@app.route('/schema-data', methods = ['GET'])
def getNodeSchemaData():
    ip = request.args.get('ip')
    schema_name = request.args.get('schema-name')
    ne_type = request.args.get('type')
    schema_data = getSchemaData(ip,ne_type,schema_name)

    return json.dumps(schema_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8081)