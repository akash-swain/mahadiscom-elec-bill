from bs4 import BeautifulSoup as bs
import requests
from time import sleep, time
import json


class GetNmmcWaterBill:
    """
    class to fetch water bill from nmmc.gov.in
    """

    def __init__(self, consumerNo):
        self.url = "https://www.nmmc.gov.in/water-bill?p_p_id=onlinewaterpayment_WAR_NMMCProjectportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_pos=1&p_p_col_count=2&_onlinewaterpayment_WAR_NMMCProjectportlet_action=consumerDetails"
        # consumerNo = self.consumerNo
        self.params = {}
        self.params["consumerNo"] = consumerNo
        self.consumerNo = consumerNo

    def getwaterbill(self):
        """ get actual bill from the consumer number"""

        try:
            response = requests.post(self.url, data=self.params)
            content = response.content
        except Exception as e:
            content = ""
            return f"exception raised: {str(e)}"

        # Get all tables from the response
        tables = bs(content, "lxml").findAll("table")
        with open("testwater.html", "w") as f:
            for table in tables:
                if table.findParent("table") is None:
                    f.write(str(table))
                    try:
                        table_data = [[cell.text.strip() for cell in row("td")]
                                      for row in table("tr")]
                        jdata = json.dumps(dict(table_data))
                        jdata = eval(jdata)
                        jdata = {str(k).replace(" ", "").replace(":",""):v for k, v in jdata.items()}
                        jdata["ConsumerNumberWater"] = self.consumerNo
                        # print (jdata)
                        # for k, v in jdata.items():
                        #     print (str(k).replace(" ", "").replace(":",""),v)
                        consumer_data = jdata["ConsumerName"]
                        return jdata
                    except:
                        print("unable to fetch data")


# Test
# start_time = time()
# custno = ["200230904", "200315138", "200231867", "200231866"]

# for cust in custno:
#     gwb = GetNmmcWaterBill(cust)
#     print(gwb.getwaterbill())
