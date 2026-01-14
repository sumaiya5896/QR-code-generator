from flask import Flask, render_template, request,url_for
import base64
import qrcode
from io import BytesIO
import os
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    qr_image=None
    file_url=None

    if request.method == 'POST':
        data = request.form.get('qrdata')

        if data:
            img=qrcode.make(data)
            buffer=BytesIO()
            img.save(buffer,format="PNG")
            buffer.seek(0)

            b64=base64.b64encode(buffer.getvalue()).decode("ascii")
            qr_image=b64

            static_folder=os.path.join(app.root_path, 'static')
            os.makedirs(static_folder, exist_ok=True)

            filename=f"qr_{int(time.time())}.png"
            file_path=os.path.join('static',filename)

            with open(file_path,'wb') as f:
                f.write(buffer.getvalue())

            file_url=url_for('static', filename=filename)

    return render_template('index.html', qr_image=qr_image,file_url=file_url,data=data if request.method == 'POST' else None)

if __name__ == '__main__':
    port= int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)