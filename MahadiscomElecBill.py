import requests
import json
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
        try:
            response = requests.post(self.url, data = self.cust_detail)
            # print (response.status_code)
            # print (dir(response))
        except Exception as e:
            print (f"{str(e)}")
        else:
            # print (response.status_code)
            json_response = json.loads(response.text)
            # print (json_response)
            if json_response:
                output_params = ["consumerNo", "netPPDAmount", "promptPaymentDiscount", "dueDate", "consumptionUnits", "billMonth", "billDate"]
                filter_json_response = {k: v for k, v in json_response.items() if k in output_params}
                return filter_json_response
            return {}

a = MahdiscomElecBillDetail("000091396297", "4641", "4")
print (a.get_bill_detail())
