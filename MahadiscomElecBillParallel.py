import requests
import json
import re
import datetime as dt
# from threading import Thread, Lock
import threading
from concurrent.futures import ThreadPoolExecutor
import requests
import threading
import time


class MahdiscomElecBillDetail():
    """
    """
    def call_parallel_elec(self, customer_list):
        with ThreadPoolExecutor(max_workers = 1) as executor:
            return executor.map(self.get_bill_detail, customer_list)


    def get_bill_detail(self, cust_no):
        """
        """
        cust_detail = {}
        cust_detail['ConsumerNo'] = cust_no
        cust_detail['BuNumber'] = "4641"
        cust_detail['consumerType'] = "4"
        url = "https://wss.mahadiscom.in/wss/wss?uiActionName=postViewPayBill&IsAjax=true"
        try:
            response = requests.post(url, data = cust_detail)
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
                # with lock:
                    # op.append(filter_json_response)
                    # print (filter_json_response)
                # return filter_json_response
                return filter_json_response
            else:
                print ("unable to fetch data")
            # op.append({})
            return {}


# aa = MahdiscomElecBillDetail()
# bb = aa.call_parallel_elec(["000091392551", "000091396297", "000098300210", "000091490978"])
# for i in bb:
#     print (i)
