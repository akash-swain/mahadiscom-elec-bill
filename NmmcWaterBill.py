from bs4 import BeautifulSoup as bs
import requests
from time import sleep, time
import json
from concurrent.futures import ThreadPoolExecutor

class GetNmmcWaterBill:
    """
    class to fetch water bill from nmmc.gov.in
    """

    def call_parallel_water(self, customer_list):
        with ThreadPoolExecutor(max_workers = 4) as executor:
            return executor.map(self.getwaterbill, customer_list)

    def getwaterbill(self, consumerNo):
        """ get actual bill from the consumer number"""
        url = "https://www.nmmc.gov.in/water-bill?p_p_id=onlinewaterpayment_WAR_NMMCProjectportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_pos=1&p_p_col_count=2&_onlinewaterpayment_WAR_NMMCProjectportlet_action=consumerDetails"
        # consumerNo = self.consumerNo
        params = {}
        params["consumerNo"] = consumerNo
        # consumerNo = consumerNo

        try:
            response = requests.post(url, data=params, timeout = 5)
            # print (response.status_code)
            content = response.content
        except Exception as e:
            # print (response.status_code)
            # content = ""
            return f"exception raised: {str(e)}"

        # Get all tables from the response
        tables = bs(content, "lxml").findAll("table")
        # with open("testwater.html", "w") as f:
        for table in tables:
            if table.findParent("table") is None:
                # f.write(str(table))
                try:
                    table_data = [[cell.text.strip() for cell in row("td")]
                                    for row in table("tr")]
                    jdata = json.dumps(dict(table_data))
                    jdata = eval(jdata)
                    jdata = {str(k).replace(" ", "").replace(":",""):v for k, v in jdata.items()}
                    jdata["ConsumerNumberWater"] = consumerNo
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

# gwb = GetNmmcWaterBill()
# aa = gwb.call_parallel_water(custno)
# for i in aa:
#     print (i)
# print (time() - start_time)