from bs4 import BeautifulSoup as bs
import requests
from time import sleep, time
import json


class GetNmmcPropertyBill:
    def __init__(self, consumerNo):
        self.url = "https://www.nmmc.gov.in/property-tax2/-/property?_onlinepropertypayment_WAR_NMMCProjectportlet_action=porpertyTax"
        self.params = {}
        self.params["propertyCode"] = consumerNo
        self.consumerNo = consumerNo

    def getpropertybill(self):

        try:
            response = requests.post(self.url, data=self.params)
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
                    jdata["ConsumerNumberProperty"] = self.consumerNo
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

start_time = time()
# prop_list = ["AI0000447039", "AI0000391342", "AI0000391318", "AI0000386076"]

# for prop in prop_list:
#     a = GetNmmcPropertyBill(prop)
#     print (a.getpropertybill())
