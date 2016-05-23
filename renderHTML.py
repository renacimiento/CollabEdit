import flask 
import redis
from PPS import PPS
app = flask.Flask(__name__)
app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
app.secret_key = 'asdf'
pps = PPS()
def listen():
    pubsub = app.redis.pubsub()
    pubsub.subscribe('collabEdit')
    for message in pubsub.listen():
    	if message["type"] != "subscribe":
    		yield 'data: %s' % message['data']

@app.route('/login', methods=["POST","GET"])
def login():
	if flask.request.method == 'POST':
		flask.session['user'] = flask.request.form['user']
		return flask.redirect('/')
	return flask.render_template('login.html')


@app.route('/')
def hello():
	pps.constructPPSFromDB(app.redis.get("content"))
	if 'user' not in flask.session:
		return flask.redirect('/login')
	return flask.render_template('main.html',content=app.redis.get("content"))

@app.route('/listen')
def stream():
    return flask.Response(listen(),
                          mimetype="text/event-stream")
@app.route('/getPPS')
def getPPS():
	return flask.jsonify(pps=pps.get_pps())

@app.route("/data", methods=["POST","GET"])
def data():
	if flask.request.method == "POST":
		app.redis.set("content", flask.request.form.get("content"))
		position = int(flask.request.form.get("position"))
		operation_type = int(flask.request.form.get("type"))
		if operation_type == 1:
		 	pps.deleteCharacter(flask.request.form.get("character"),position)
		else:
			pps.insertCharacter(flask.request.form.get("character"),position)
		app.redis.publish("collabEdit",flask.request.form.get("content"))
		return flask.jsonify(success=True)
	elif flask.request.method == "GET":
		return flask.jsonify(data=app.redis.get("content"))

if __name__ == "__main__":
	app.debug=True
	#app.run(host= '0.0.0.0',threaded=True)
	app.run(threaded=True) 
