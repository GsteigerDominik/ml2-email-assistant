from flask import Flask, send_file, request, jsonify
from flask_cors import CORS

from service.conversation_handler import ConversationHandler

print("*** Init Flask App ***")
app = Flask(__name__, static_url_path='/', static_folder='static')
cors = CORS(app)
conversation_handler = ConversationHandler()


@app.route("/")
def indexPage():
    return send_file("static/index.html")


@app.route('/parse-email', methods=['POST'])
def parse_email():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        response = conversation_handler.parse_email(file)
        return jsonify({'response': response})


@app.route('/upload-email', methods=['POST'])
def upload_email():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        response = conversation_handler.handle_email(file)
        return jsonify({'response': response})


@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message', '')
    if message:
        response = conversation_handler.handle_user_input(message)
        print('hey',response)
        return jsonify({'response': response})
    return jsonify({'error': 'No message provided'}), 400


@app.route("/clear", methods=['POST'])
def clear():
    conversation_handler.__init__()
    return jsonify({'response': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
