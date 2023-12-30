from flask import Flask, jsonify, request
from utils import load_model

app = Flask(__name__)

BASE_URI = "/api/v1/{path}"

model = load_model()

@app.route(BASE_URI.format(path="recommendations"), methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id')
    k = request.args.get('k', 5)
    k = int(k)
    user_id = int(user_id)
    recommendations = model.get_top_k_recommendations(user_id, k)
    return jsonify({'user_id': user_id, 'recommendations': recommendations})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=6000)