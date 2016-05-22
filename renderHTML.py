import flask 
import redis
app = flask.Flask(__name__)
app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
app.secret_key = 'asdf'

def listen():
    pubsub = app.redis.pubsub()
    pubsub.subscribe('collabEdit')
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']

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

@app.route("/data", methods=["POST","GET"])
def data():
	if flask.request.method == "POST":
		app.redis.set("content", flask.request.form.get("content"))
		app.redis.publish("collabEdit",flask.request.form.get("content"))
		return flask.jsonify(success=True)
	elif flask.request.method == "GET":
		return flask.jsonify(data=app.redis.get("content"))

if __name__ == "__main__":
	app.debug=True
	app.run(host= '0.0.0.0',threaded=True) 
