# 使用Python中的FastAPI串接藍新金流
## 敘述
本repo使用python語言中的FastAPI串接[藍新金流](https://www.newebpay.com/)，並以**信用卡定期定額**為範例。
## 安裝指南
在開始使用之前，請確保你已經完成以下事項：
 - 建立藍新金流帳戶及商店
 - 安裝[Pyhon](https://www.python.org/)
 - 具有基本HTTP Request知識
本repo並不包含前端架設，若要實現`form`表單跳轉操作，可使用[W3Schools 線上編輯器](https://www.w3schools.com/html/tryit.asp?filename=tryhtml_default_default)操作。
## 使用指南
1. 從藍新金流[商店頁面](https://cwww.newebpay.com/shop/member_shop/shop_list)中，點選`詳細資料`。
2. 獲取`key`(HashKey), `iv`(HashIV) 以及`mid`(商店代號)。
3. 打開 `main.py` ，宣告`key`, `iv`以及`mid`的值。範例：
```
key = 'AAAvw3YlqoEk6G4HqRKDAYpHKZWxBBB'
iv = 'AAAC1FplieBBB'
mid = 'MS12345678'
```
4. 進入專案資料夾，於終端輸入`uvicorn main:app --port=4201 --reload`，你便能在[http://localhost:4201/docs](http://localhost:4201/docs)上看到自動生成的Swagger UI。
5. POST `http://localhost:4201/order/postData`Request Body中註明付款金額和用戶信箱。範例：
```
{
  "price": 30,
  "email": "user@example.com"
}
```
6. 你將會獲得`MerchantID_`以及`PostData_`，填入form表單中對應的`value`欄位後，按下提交(submit)按鈕。
```
<form action="https://ccore.newebpay.com/MPG/period" id="form" method="post">
  <input hidden name="MerchantID_" value="">
  <input hidden name="PostData_" value="">
  <input type="submit">
</form>
```
7. 使用測試信用卡`4000-2211-1111-1111`付款後，畫面便會顯示回傳結果。
## 常見問題
 - 若在運行Python時出了問題，請確保`import`所使用的module都已經安裝，可使用以下指令替換`<moduleName>`安裝缺少的module：
```
pip install <moduleName>
```
## 參考文獻
- [藍新金流 - API文件 - 信用卡定期定額](https://www.newebpay.com/website/Page/download_file?name=Credit%20Card%20Periodic%20Payment%20API%20Specification_NDNP-1.0.0.pdf)
