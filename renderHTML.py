import flask 
import redis
import json
import time
from PPS import PPS
from hot_redis import Dict, List, Queue, transaction
app = flask.Flask(__name__)
app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
app.secret_key = 'asdf'
pps = PPS()
def listen():
	pubsub = app.redis.pubsub()
	pubsub.subscribe('collabEdit')
	lst = []
	print "HERE"
	for message in pubsub.listen():
		if message["type"] != "subscribe":
			yield 'data: %s\n\n' % message['data']

def str_to_bool(s):
    if s == 'true':
         return True
    elif s == 'false':
         return False
    else:
         raise ValueError # evil ValueError that doesn't tell you what the wrong value was

@app.route('/login', methods=["POST","GET"])
def login():
	if flask.request.method == 'POST':
		flask.session['user'] = flask.request.form['user']
		return flask.redirect('/')
	return flask.render_template('login.html')

@app.route('/')
def hello():
	if 'user' not in flask.session:
		return flask.redirect('/login')
	return flask.render_template('main.html')

@app.route('/listen')
def stream():
    return flask.Response(listen(),
                          mimetype="text/event-stream")

def post():
	data = {}
	data["value"] = str(flask.request.form.get("value"))
	data["positionStamp"] = float(flask.request.form.get("positionStamp"))
	data["state"] = str(flask.request.form.get("state"))
	data["clientID"] = str(flask.request.form.get("clientID"))
	app.redis.publish("collabEdit",data)	

@app.route("/data", methods=["POST"])
def data():
	post()
	return flask.jsonify(success=True)

def shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == "__main__":
	app.debug=True
	app.run(host= '0.0.0.0',threaded=True)
	#app.run(threaded=True) 
