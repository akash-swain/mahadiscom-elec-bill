from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from MahadiscomElecBill import MahdiscomElecBillDetail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import ConDetail
from django.contrib import messages
# Create your views here.

# class BillList(LoginRequiredMixin, ListView):
#     template_name = "billapp/billdetail.html"
#     login_url = '/login/'
#     # redirect_field_name = reverse_lazy("detail")


    # def get_context_data(self, *args, **kwargs):
    #     context = super(BillList, self).get_context_data(*args, **kwargs)
    #     customer = {"Q/121": "000091396297","U/20": "000098300210","R/71-L": "000091490978","R/72-R": "000091392551"}
    #     t = []
    #     total_bill = 0
    #     for add, cust in customer.items():
    #         obj_bill = MahdiscomElecBillDetail(cust, "4641", "4")
    #         data = obj_bill.get_bill_detail()
    #         data["add"] = add
    #         total_bill += data.get("netPPDAmount", 0)
    #         t.append(data)
    #     # print (t)
    #     context["data"] = t
    #     context["total_bill"] = total_bill
    #     # print (context)
    #     return context
    #
    # def get_queryset(self):
    #     user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     return User.objects.filter(username=user)


class BillList(LoginRequiredMixin,ListView):
    template_name = "billapp/billdetail.html"
    login_url = '/login/'
    model = ConDetail
    # context_object_name = "usercon"
    # template_name = "billapp/billdetail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BillList, self).get_context_data(*args, **kwargs)
        # print (context["object_list"])
        self.customers = context["condetail_list"]
        # print (customer)
        t = []
        total_bill = 0
        for cust in self.customers:
            obj_bill = MahdiscomElecBillDetail(cust, "4641", "4")
            data = obj_bill.get_bill_detail()
            total_bill += data.get("netPPDAmount", 0)
            t.append(data)
        # print (t)
        context["data"] = t
        context["total_bill"] = total_bill
        # print (context)
        return context
    # ordering = ["-date_posted"]
    # paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        consumer_list = ConDetail.objects.filter(consumer__username = user)
        return consumer_list

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user.username)
        try:
            post_data = request.POST["content"]
            check_in_current = ConDetail.objects.get(consumerno = post_data, consumer = user)
        except ConDetail.DoesNotExist:
            obj_bill = MahdiscomElecBillDetail(post_data, "4641", "4")
            data = obj_bill.get_bill_detail()
            if data:
                user = get_object_or_404(User, username=self.request.user.username)
                c1 = ConDetail(consumerno = post_data, consumer = user)
                c1.save()
                # return redirect("detail")
                messages.success(request, f'Consumer {post_data} added successfully.')
                return redirect("detail")
            messages.error(request, f'Consumer {post_data} is invalid.')
            return redirect("detail")
        else:
            messages.error(request, f'Consumer {post_data} already exists.')
            return redirect("detail")


    # def get(self, request, *args, **kwargs):
    #     # c1 = Todo.objects.get(id = id)
    #     # c1.delete()
    #     return redirect("detail")
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     print (form)
        #     # <process form cleaned data>
        #     return HttpResponseRedirect('/success/')
        # return render(request, self.template_name, {'form': form})

class ThanksPage(TemplateView):
    template_name = "billapp/logout.html"


def listdelete(request, consumerno):
    try:
        print (consumerno)
        user = get_object_or_404(User, username=request.user.username)
        print (user)
        query = ConDetail.objects.get(consumerno=consumerno, consumer = user)
        print (query)
        query.delete()
        return redirect("detail")
    except Exception as e:
        print (str(e))
        return redirect("detail")

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
