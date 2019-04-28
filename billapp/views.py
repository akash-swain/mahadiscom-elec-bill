from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from MahadiscomElecBill import MahdiscomElecBillDetail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
# Create your views here.

class BillList(LoginRequiredMixin, TemplateView):
    template_name = "billapp/billdetail.html"
    login_url = '/login/'
    redirect_field_name = reverse_lazy("detail")


    def get_context_data(self, *args, **kwargs):
        context = super(BillList, self).get_context_data(*args, **kwargs)
        customer = {"Q/121": "000091396297","U/20": "000098300210","R/71-R": "000091490978","R/72-L": "000091392551"}
        t = []
        total_bill = 0
        for add, cust in customer.items():
            obj_bill = MahdiscomElecBillDetail(cust, "4641", "4")
            data = obj_bill.get_bill_detail()
            data["add"] = add
            total_bill += data["netPPDAmount"]
            t.append(data)
        # print (t)
        context["data"] = t
        context["total_bill"] = total_bill
        # print (context)
        return context




class ThanksPage(TemplateView):
    template_name = "billapp/logout.html"
