import json
import time as T
from datetime import datetime as DT
from typing import Annotated

import requests as rq
import uvicorn
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

key = ''
iv = ''
mid = ''

def openssl_encrypt(data, key, iv):
   data = bytes(data, 'utf-8')
   key = bytes(key, 'utf-8')
   iv = bytes(iv, 'utf-8')

   backend = default_backend()

   cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

   encryptor = cipher.encryptor()   
   padder = padding.PKCS7(algorithms.AES.block_size).padder()

   padded_data = padder.update(data) + padder.finalize()
   encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

   return encrypted_data

def strippadding(data):
    last_byte = data[-1]
    padding_size = last_byte if isinstance(last_byte, int) else ord(last_byte)
    return data[:-padding_size]

def openssl_decrypt(encrypted_data, key, iv):
   encrypted_data = bytes.fromhex(encrypted_data)
   key = bytes(key, 'utf-8')
   iv = bytes(iv, 'utf-8')

   backend = default_backend()

   cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
   decryptor = cipher.decryptor()

   decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

   return strippadding(decrypted_data).decode('utf-8')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
)

class OrderPostDataReqAttr(BaseModel):
   price: int
   email: str

class OrderModifyReqAttr(BaseModel):
   orderNo: str
   periodNo: str

@app.post("/order/postData")
async def read_item(req: OrderPostDataReqAttr):
   timestamp = int(T.time())
   date = DT.strftime(DT.now(), '%d')
   orderConfig = {
      'RespondType': 'JSON', # 回傳格式
      'TimeStamp': timestamp, # 時間戳記
      'Version': '1.5', # 串接程式版本
      'LangType': 'zh-Tw', # 語系
      'MerOrderNo': f'myOrder{timestamp}', #商店訂單編號
      'ProdDesc': 'MyProductName', # 產品名稱
      'PeriodAmt': req.price, # 委託金額
      'PeriodType': 'M', # 週期類別
      'PeriodPoint': date, # 交易週期授權時間（扣款日）
      'PeriodStartType': '2', # 交易模式
      'PeriodTimes': '12', # 授權期數
      'PaymentInfo': 'N', #是否開啟付款人資訊
      'OrderInfo': 'N', #是否開啟收件人資訊
      'EmailModify': '0', # 付款人電子信箱是否開放修改
      'ReturnURL': 'http://localhost:4201/order/handle', # 返回商店網址
      'PayerEmail': req.email, # 付款人電子信箱
   }
   orderConfigString = '&'.join([f'{key}={orderConfig[key]}' for key in orderConfig.keys()])
   edata1 = openssl_encrypt(orderConfigString, key, iv).hex()

   data = {
      'MerchantID_': mid, # 藍新金流商店代號
      'PostData_': edata1 # AES 加密後的資料
   }

   return data

@app.post("/order/handle")
def paymentSuccess(Period: Annotated[str, Form()]):
   res = json.loads(openssl_decrypt(Period, key, iv))

   return res

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")