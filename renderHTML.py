import flask 
import redis
from PPS import PPS
from hot_redis import Dict, List, Queue, transaction
app = flask.Flask(__name__)
app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
app.secret_key = 'asdf'
pps = PPS()
def listen():
	pubsub = app.redis.pubsub()
	pubsub.subscribe('collabEdit')
	for message in pubsub.listen():
		print message
    	if message["type"] != "subscribe":
    		yield 'data: %s' % message['data']

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
	#pps.constructPPSFromDB(app.redis.get("content"))
	if 'user' not in flask.session:
		return flask.redirect('/login')
	return flask.render_template('main.html')

@app.route('/listen')
def stream():
    return flask.Response(listen(),
                          mimetype="text/event-stream")

def post():
	c = flask.request.form.get("character")
	app.redis.set("content", flask.request.form.get("content"))
	positionStamp = int(flask.request.form.get("positionStamp"))
	characterState = str_to_bool(flask.request.form.get("state"))
	data = {}
	data["character"] = c
	data["positionStamp"] = positionStamp
	data["state"] = characterState
	app.redis.publish("collabEdit",flask.request.form.get("content"))
	print "PUBLISHED"

# @app.route('/getPPS')
# def getPPS():
# 	return flask.jsonify(pps=pps.get_pps())

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
