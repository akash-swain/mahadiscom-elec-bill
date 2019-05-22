from bs4 import BeautifulSoup as bs
import requests
from time import sleep, time
import json
from concurrent.futures import ThreadPoolExecutor



class GetNmmcPropertyBill:


    def call_parallel_property(self, customer_list):
        with ThreadPoolExecutor(max_workers = 4) as executor:
            return executor.map(self.getpropertybill, customer_list)

    def getpropertybill(self, consumerNo):
        url = "https://www.nmmc.gov.in/property-tax2/-/property?_onlinepropertypayment_WAR_NMMCProjectportlet_action=porpertyTax"
        params = {}
        params["propertyCode"] = consumerNo

        try:
            response = requests.post(url, data=params)
        except Exception as e:
            content = ""
            return f"exception raised: {str(e)}"
        else:
            content = response.content
            # print(content)
            # with open("testop.html", "w") as f:
            #     f.write(str(content))

        tables = bs(content, "lxml").findAll(attrs={"class": "table"})

        # with open("testwater.html", "w") as f:
        for table in tables:
            if table.findParent("table") is None:
                # f.write(str(table))
                # print (table)
                try:
                    table_data = [[cell.text.strip() for cell in row("td")]
                                    for row in table("tr")]
                    jdata = json.dumps(dict(table_data))
                    jdata = eval(jdata)
                    jdata = {str(k).replace(" ", "").replace(":",""):v for k, v in jdata.items()}
                    jdata["ConsumerNumberProperty"] = consumerNo
                    # print (jdata)
                    # for k, v in jdata.items():
                    #     print (str(k).replace(" ", "").replace(":",""),v)
                    consumer_data = jdata["OwnerName"]
                    return jdata
                except Exception as e:
                    print("unable to fetch data")
    # for table in tables:
    #     if table.findParent("table") is None:
    #         print(str(table))

# start_time = time()
# prop_list = ["AI0000447039", "AI0000391342", "AI0000391318", "AI0000386076"]

# a = GetNmmcPropertyBill()
# aa = a.call_parallel_property(prop_list)
# for i in aa:
#     print (i)
# print (time() - start_time)
