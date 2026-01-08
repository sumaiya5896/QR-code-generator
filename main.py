from flask import Flask, render_template, request
import qrcode
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, 'static')

@app.route('/', methods=['GET', 'POST'])
def home():
    qr_file=None

    if request.method == 'POST':
        data = request.form.get('qrdata')

        if data:
            os.makedirs(STATIC_DIR, exist_ok=True)  # Ensure the static directory exists
            img = qrcode.make(data) 
            img.save(os.path.join(STATIC_DIR, "qr.png"))
            qr_file = "qr.png"  

    return render_template('index.html', qr_file=qr_file)
if __name__ == '__main__':
    app.run(debug=True)