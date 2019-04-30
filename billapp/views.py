from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from MahadiscomElecBill import MahdiscomElecBillDetail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Create your views here.

class BillList(LoginRequiredMixin, TemplateView):
    template_name = "billapp/billdetail.html"
    login_url = '/login/'
    # redirect_field_name = reverse_lazy("detail")


    def get_context_data(self, *args, **kwargs):
        context = super(BillList, self).get_context_data(*args, **kwargs)
        customer = {"Q/121": "000091396297","U/20": "000098300210","R/71-R": "000091490978","R/72-L": "000091392551"}
        t = []
        total_bill = 0
        for add, cust in customer.items():
            obj_bill = MahdiscomElecBillDetail(cust, "4641", "4")
            data = obj_bill.get_bill_detail()
            data["add"] = add
            total_bill += data.get("netPPDAmount", 0)
            t.append(data)
        # print (t)
        context["data"] = t
        context["total_bill"] = total_bill
        # print (context)
        return context




class ThanksPage(TemplateView):
    template_name = "billapp/logout.html"


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Electricity bill account'
            # message = render_to_string('billapp/acc_active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            #     'token':account_activation_token.make_token(user),
            # })
            message = f"Hi {user}, \n Please click below link to activate your account:  \n http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk)).decode()}/{account_activation_token.make_token(user)} \n \n Thanks, \n Akash Swain"
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse(f'Thanks {user} \n Please check your mailbox and verify your account - {to_email}')
    else:
        form = SignupForm()
    return render(request, 'billapp/signup.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse(f'Thank you for your email confirmation. Login - {get_current_site(request).domain}.')
    else:
        return HttpResponse('Activation link is invalid!')
