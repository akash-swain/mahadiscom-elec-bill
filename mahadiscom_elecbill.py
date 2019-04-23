import requests
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
        except Exception as e:
            print (f"{str(e)}: {response.status_code}" )
        else:
            # print (response.status_code)
            json_response = response.json()
            if json_response:
                output_params = ["netPPDAmount", "promptPaymentDiscount", "dueDate", "consumptionUnits", "billMonth", "billDate"]
                filter_json_response = {k: v for k, v in json_response.items() if k in output_params}
                return filter_json_response
            return {}


cust_list = ("000091396297", "000098300210", "000091490978", "000091392551", "")
for cust in cust_list:
    user_object = MahdiscomElecBillDetail(cust, "4641", "4")
    print (user_object.get_bill_detail())
