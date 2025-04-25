import base64
import os
from urllib.parse import quote_plus

MYSQL_DB_NAME = os.getenv('MYSQL_DB_NAME', "donate")
MYSQL_DB_USER = os.getenv('MYSQL_DB_USER', "dmlzaHdh")
MYSQL_DB_PASSWORD = os.getenv('MYSQL_DB_PASSWORD', "password")
MYSQL_DB_PORT = os.getenv('MYSQL_DB_PORT', "3306")
MYSQL_DB_HOST = os.getenv('MYSQL_DB_HOST', "localhost")
WEB_PORT = int(os.getenv('WEB_PORT', 14011))



MYSQL_CONNECTION = "{}:{}@{}:{}/{}".format(MYSQL_DB_USER, MYSQL_DB_PASSWORD, MYSQL_DB_HOST, MYSQL_DB_PORT,
                                           MYSQL_DB_NAME)

print(f"{MYSQL_CONNECTION=}")

# PayPal Configuration
PAYPAL_CLIENT_ID: str = os.getenv("PAYPAL_CLIENT_ID", "AcftZHTd7jkmqFILGvJWi93kt1LUEAHDsLW6Wmh5fCFNJ75k8mLkMeDS1QbAkLPd8F-xjJMEoE0Rm")
PAYPAL_CLIENT_SECRET: str = os.getenv("PAYPAL_CLIENT_SECRET", "EIQJ1V3xyaEceJYlDQoEYRJmxokjAbESrn1B52x3uwfMAXqFw-May9QAupZOeSMWk0QIHPS_-EeYl")
FRONT_END_URL: str = os.getenv("FRONT_END_URL", "https://626d-152-59-38-172.ngrok-free.app")

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440