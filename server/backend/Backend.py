import json
from flask import Flask, Response
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app)

# Initialize Redis connection
redis_client = redis.StrictRedis(host='103.90.73.217', port=6379, db=0)

def generate():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('my_channel')  # Subscribe to a Redis channel

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            yield f"data: {json.dumps(data)}\n\n"

@app.route('/stream')
def stream():
    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8001)
