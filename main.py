from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel

import qrMaker

FILENAME = "qr.png"
SENDER_EMAIL = "asendiumteam@gmail.com"
PASSWORD = "graoktexmxemevut"

class Emailer (BaseModel):
    email: str
    link: str
    

app = FastAPI(docs_url="/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/sed")
def name(word: str):
    return {"message": word}
    
# end def

@app.get("/emailsender")
def send_qrcode_by_email(emailer: Emailer):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Enlace de descarga"
        msg["From"] = SENDER_EMAIL
        msg["To"] = emailer.email

        qrMaker.create_qr(FILENAME, emailer.link)

        with open(FILENAME, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            "attachment", filename=FILENAME
        )
        msg.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(
                SENDER_EMAIL, emailer.email, msg.as_string()
            )
        return {"message": "Email sent successfully"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost',
                port=8099, reload=True, debug=True)
