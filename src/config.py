import os
from dotenv import load_dotenv


load_dotenv()

USERNAME = os.getenv("SICONT_USERNAME")
PASSWORD = os.getenv("SICONT_PASSWORD")

LOGIN_PAGE_URL = 'http://ctp.sudoesteinformatica.com.br/webrun/open.do?action=open&sys=CTP'