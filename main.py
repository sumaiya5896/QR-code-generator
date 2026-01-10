from flask import Flask, render_template, request
import base64
import qrcode
import os
from io import BytesIO
from PIL import Image

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

@app.route('/download')
def download_qr():
    b64_png = request.args.get('qr_image')
    if not b64_png:
        return "No QR code image found", 400
    import base64
    from io import BytesIO

    try:
        png_bytes=base64.b64decode(b64_png)
    except Exception:
        return "Invalid QR code image data", 400
    return send_file(BytesIO(png_bytes), mimetype='image/png', as_attachment=True, download_name='qr_code.png')

if __name__ == '__main__':
    port= int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)