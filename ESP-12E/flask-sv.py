from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/time')
def getTime():
    time = datetime.now()
    return "Hotspot date and time: " + str(time)

@app.route('/brokerIp')
def getBrokerId():
    return "129.69.185.169"

@app.route('/brokerTopic')
def getBrokerTopic():
    return "test"

app.run(host='0.0.0.0', port=8090)

