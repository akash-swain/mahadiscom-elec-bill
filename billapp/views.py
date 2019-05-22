from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from MahadiscomElecBill import MahdiscomElecBillDetail
from MahadiscomElecBillParallel import MahdiscomElecBillDetail as mad
from NmmcWaterBill import GetNmmcWaterBill
from NmmcTaxBill import GetNmmcPropertyBill
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
from .models import ConDetail, ConDetailWater, ConDetailProperty
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
        # print (context["object_list"][0])
        # self.customers = context["condetail_list"]
        self.customers = context["object_list"][0]
        # self.customer_water = context["consumer_list_water"]
        self.customer_water = context["object_list"][1]
        self.customer_property = context["object_list"][2]
        # print (customer)
        with open("bu_list.txt", "r") as f:
            bu_list = eval(f.read())
            # print (bu_list)
        t = []
        total_bill = 0
        # for cust in self.customers:
        #     obj_bill = MahdiscomElecBillDetail(cust, "4641", "4")
        #     data = obj_bill.get_bill_detail()
        #     try:
        #         total_bill += data.get("netPPDAmount", 0)
        #         t.append(data)
        #     except Exception as e:
        #         total_bill = 0
        obj_bill = mad()
        t = list(obj_bill.call_parallel_elec(self.customers))
        
        # water bill fetch
        w = []
        total_bill_water = 0
        # for cust in self.customer_water:
        #     obj_bill_water = GetNmmcWaterBill(cust)
        #     data_water = obj_bill_water.getwaterbill()
        #     try:
        #         total_bill_water += float(data_water.get("Outstanding", 0))
        #         w.append(data_water)
        #     except Exception as e:
        #         total_bill_water = 0
        obj_bill_water = GetNmmcWaterBill()
        w = list(obj_bill_water.call_parallel_water(self.customer_water))


        # property bill fetch
        p = []
        total_bill_property = 0
        # for cust in self.customer_property:
        #     obj_bill_property = GetNmmcPropertyBill(cust)
        #     data_property = obj_bill_property.getpropertybill()
        #     try:
        #         total_bill_property += float(data_property.get("Outstanding", 0))
        #         p.append(data_property)
        #     except Exception as e:
        #         total_bill_property = 0
        obj_bill_property = GetNmmcPropertyBill()
        p = list(obj_bill_property.call_parallel_property(self.customer_property))

        # print (t)
        context["data"] = t
        context["data_water"] = w 
        context["data_property"] = p
        context["total_bill"] = total_bill
        context["total_bill_water"] = total_bill_water
        context["total_bill_property"] = total_bill_property
        context["bu"] = bu_list
        # print (context)
        return context
    # ordering = ["-date_posted"]
    # paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        consumer_list = ConDetail.objects.filter(consumer__username = user)
        consumer_list_water = ConDetailWater.objects.filter(consumer__username = user)
        consumer_list_property = ConDetailProperty.objects.filter(consumer__username = user)

        return consumer_list , consumer_list_water, consumer_list_property


    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user.username)

        get_form = request.POST.get("content", "invalid-form")
        if get_form == "invalid-form":
            get_form = request.POST.get("content_water", "invalid-form")
            if get_form == "invalid-form":
                get_form = request.POST.get("content_property", "invalid-form")
                if get_form == "invalid-form":
                    print ("incorrect form data")
                else:
                    form_flag = "content_property"    
            else:
                form_flag = "content_water"    
        else:
            form_flag = "content"

        if form_flag == "content":
            try:
                post_data = request.POST["content"]
                area = request.POST["area"]
                check_in_current = ConDetail.objects.get(consumerno = post_data, consumer = user)
            except ConDetail.DoesNotExist:
                obj_bill = MahdiscomElecBillDetailParallel()
                data = obj_bill.get_bill_detail(post_data)
                if data:
                    user = get_object_or_404(User, username=self.request.user.username)
                    c1 = ConDetail(consumerno = post_data, consumer = user)
                    c1.save()
                    # return redirect("detail")
                    messages.success(request, f'Consumer {post_data} added successfully.', extra_tags='electricity')
                    return redirect("detail")
                messages.error(request, f'Consumer {post_data} is invalid.', extra_tags='electricity')
                return redirect("detail")
            else:
                messages.error(request, f'Consumer {post_data} already exists.', extra_tags='electricity')
                return redirect("detail")


        # Added for Water Bill
        if form_flag == "content_water":
            try:
                post_data = request.POST["content_water"]
                check_in_current = ConDetailWater.objects.get(consumerno = post_data, consumer = user)
            except ConDetailWater.DoesNotExist:
                # obj_bill_water = GetNmmcWaterBill(post_data)
                obj_bill_water = GetNmmcWaterBill()
                data = obj_bill_water.getwaterbill(post_data)
                if data:
                    user = get_object_or_404(User, username=self.request.user.username)
                    c1 = ConDetailWater(consumerno = post_data, consumer = user)
                    c1.save()
                    # return redirect("detail")
                    messages.success(request, f'Consumer {post_data} added successfully.', extra_tags='water')
                    return redirect("detail")
                messages.error(request, f'Consumer {post_data} is invalid.', extra_tags='water')
                return redirect("detail")
            else:
                messages.error(request, f'Consumer {post_data} already exists.', extra_tags='water')
                return redirect("detail")


        # Added for Property Bill
        if form_flag == "content_property":
            try:
                post_data = request.POST["content_property"]
                check_in_current = ConDetailProperty.objects.get(consumerno = post_data, consumer = user)
            except ConDetailProperty.DoesNotExist:
                obj_bill_property = GetNmmcPropertyBill()
                data = obj_bill_property.getpropertybill(post_data)
                if data:
                    user = get_object_or_404(User, username=self.request.user.username)
                    c1 = ConDetailProperty(consumerno = post_data, consumer = user)
                    c1.save()
                    # return redirect("detail")
                    messages.success(request, f'Consumer {post_data} added successfully.', extra_tags='property')
                    return redirect("detail")
                messages.error(request, f'Consumer {post_data} is invalid.', extra_tags='property')
                return redirect("detail")
            else:
                messages.error(request, f'Consumer {post_data} already exists.', extra_tags='property')
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

# class ThanksPage(TemplateView):
#     template_name = "billapp/logout.html"


def listdelete(request, consumerno):
    try:
        # print (consumerno)
        user = get_object_or_404(User, username=request.user.username)
        # print (user)
        query = ConDetail.objects.get(consumerno=consumerno, consumer = user)
        # print (query)
        query.delete()
        return redirect("detail")
    except Exception as e:
        # print (str(e))
        return redirect("detail")

def listdeletewater(request, consumerno):
    try:
        # print (consumerno)
        user = get_object_or_404(User, username=request.user.username)
        # print (user)
        query = ConDetailWater.objects.get(consumerno=consumerno, consumer = user)
        # print (query)
        query.delete()
        return redirect("detail")
    except Exception as e:
        # print (str(e))
        return redirect("detail")


def listdeleteproperty(request, consumerno):
    try:
        # print (consumerno)
        user = get_object_or_404(User, username=request.user.username)
        # print (user)
        query = ConDetailProperty.objects.get(consumerno=consumerno, consumer = user)
        # print (query)
        query.delete()
        return redirect("detail")
    except Exception as e:
        # print (str(e))
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
