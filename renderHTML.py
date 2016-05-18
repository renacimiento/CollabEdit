from flask import Flask, render_template, request, jsonify
import redis
app = Flask(__name__)
app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def hello():
    return render_template('main.html')

@app.route("/data", methods=["POST","GET"])
def data():
	if request.method == "POST":
		app.redis.set("content", request.form.get("content"))
		return jsonify(success=True)
	elif request.method == "GET":
		return jsonify(data=app.redis.get("content"))

if __name__ == "__main__":
    app.run() 
