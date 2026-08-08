from langchain.chat_models import init_chat_model
import flask

from flask import Flask, request, jsonify

app = Flask(__name__)


GOOGLE_API_KEY = 'AIzaSyCG0DullANSHD0ePJTGl6F0crGjHzG-QGg'

model = init_chat_model(
                model="llama3.2:1b",
                model_provider="ollama"
            )


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    response = model.invoke(question)
    # return jsonify({'response': response.content})
    return jsonify({
        'message': {"role": "assistant", "content": response.content},
    })

# response = model.invoke("which having best scope in the future in india context what will be the probable salary for 10 years of experience?")
# print(response.text)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
