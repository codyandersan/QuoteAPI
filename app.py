from flask import Flask, send_file, request
from main import create_image

app = Flask(__name__)


@app.route('/')
def home():
    return 'Visit: <pre style="display:inline;"><code>/get_image?interests=motivation,inspiration</code></pre> endpoint to create and download an image'


@app.route('/get_image')
def get_image():
    interests = request.args.get('interests')
    # Call process_image function from main.py here
    image = create_image("")
    return send_file(image, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)