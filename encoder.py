import jwt
import datetime
import time
from jwt import ExpiredSignatureError


def encode_data(json_data, secret):
    json_data['exp'] = datetime.datetime.utcnow()+datetime.timedelta(seconds=600)
    json_data['data'] = str(datetime.datetime.utcnow())
    return jwt.encode(payload=json_data, key=secret, algorithm='HS256')



def decode_data(token, secret):
    try:
        data = jwt.decode(jwt = token, key=secret, algorithms='HS256')
        status = True
    except Exception as e:
        data = e
        status = False
    return data,status



# secret = 'Pounded yam'
# json_data = {
#             'name':'Oladapo',
#              'email':'o@a.com'

#              }
# head = {
#         'alg': 'HS256',
#         'typ':'JWT'
#         }


# token = encode_data(json_data, secret )
# print(token)
# time.sleep(20)

# print(decode_data(token,secret))
