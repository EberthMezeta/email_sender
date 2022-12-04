import pyqrcode

def create_qr(filename, link):
    content = link
    qrcode = pyqrcode.create(content)
    qrcode.png(filename, scale=5)
