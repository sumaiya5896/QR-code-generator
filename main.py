from flask import Flask, render_template, request
import base64
import qrcode
from io import BytesIO
import os
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    qr_image=None
    

    if request.method == 'POST':
        data = request.form.get('qrdata')

        if data:
            img=qrcode.make(data)
            buffer=BytesIO()
            img.save(buffer,format="PNG")
            buffer.seek(0)

            b64=base64.b64encode(buffer.getvalue()).decode("ascii")
            qr_image=b64

    return render_template('index.html', qr_image=qr_image)

if __name__ == '__main__':
    port= int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)