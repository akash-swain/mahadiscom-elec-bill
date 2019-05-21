import requests
import json
import re
import datetime as dt

class MahdiscomElecBillDetail():
    """
    """
    def __init__(self, cust_no, bill_unit, consumer_type):
        self.cust_detail = {}
        self.cust_detail['ConsumerNo'] = cust_no
        self.cust_detail['BuNumber'] = bill_unit
        self.cust_detail['consumerType'] = consumer_type
        self.url = "https://wss.mahadiscom.in/wss/wss?uiActionName=postViewPayBill&IsAjax=true"

    def get_bill_detail(self):
        """
        """
        try:
            response = requests.post(self.url, data = self.cust_detail)
            # print (response.status_code)
            # print (dir(response))
        except Exception as e:
            print (f"{str(e)}")
        else:
            json_response = json.loads(response.text)
            if isinstance(json_response, dict):
                pattern = r"\d{10}"
                # print (json_response["promptPaymentDate"])
                result = re.findall(pattern, json_response.get("promptPaymentDate","Unable to fetch"))
                json_response["promptPaymentDate"] = dt.date.fromtimestamp(int(result[0])).strftime('%d-%m-%Y') if result[0:] else 0
                output_params = ["consumerNo", "netPPDAmount", "promptPaymentDiscount", "promptPaymentDate" ,"dueDate", "consumptionUnits", "billMonth", "billDate", "billToBePaid"]
                filter_json_response = {k: v for k, v in json_response.items() if k in output_params}
                return filter_json_response
            return {}




aa = MahdiscomElecBillDetail("700006278711", "4703", "4")
print (aa.get_bill_detail())