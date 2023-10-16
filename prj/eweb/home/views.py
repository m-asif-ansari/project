from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from home.models import Customer
from home.forms import CustForm
from datetime import datetime, timedelta
from django.db.models import Sum, Count
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random
from django.contrib.auth.decorators import login_required



def home_index(request):
    return render(request, 'home_index.html')


@login_required
def dashboard(request):
    due = Customer.objects.aggregate(Sum('bal'))
    pending = Customer.objects.filter(status='False').count()
    paid_month = month_date(request)
    paid_today = today_date(request)
    return render(request, 'dindex.html', {'due':due['bal__sum'], 'pending':pending, 'paid_month':paid_month, 'paid_today':paid_today})

def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'dashboard.html')
    else:
        return HttpResponse("invalid login")
    

def logout(request):
    user = authenticate(request)
    logout(request, user)
    return render(request, 'home_index.html')

@login_required
def entry(request):
    context = {}
    form = CustForm(request.POST or None, request.FILES or None)
   
    if form.is_valid():
        form.save()
        messages.success(request, "Entry Inserted Successfully" )
        return HttpResponseRedirect('/entry')
    context['form']= form

    return render(request, "entry.html", context)


@login_required
def task(request):
    cust = Customer.objects.all()
    return render(request, 'task.html',  {'cust':cust })


@login_required
def pending(request):
    cust =  Customer.objects.filter(status='False').values()
    return render(request, 'pending_task.html', {'cust':cust})


@login_required
def due(request):
    cust =  Customer.objects.all().filter(bal__gt= 1).values()
    return render(request, 'due.html', {'cust':cust })


@login_required
def update_pending(request,id):
    cust = Customer.objects.get(id=id)
    cust.status=True
    cust.save()
    messages.success(request, "Status Updated to Completed" )
    c = Customer.objects.filter(status='False').values()
    return render(request, 'pending_task.html', {'cust':c})
    

@login_required
def update_paid_amt(request, id):
    cust = Customer.objects.get(id=id)
    update_paid=request.POST.get('update_amt') or 0
    cust.paid = cust.paid+int(update_paid)
    cust.save()
    messages.success(request, "Paid Amount Updated" )
    c = Customer.objects.all().values()
    return render(request, 'due.html', {'cust':c})


@login_required
def bill(request,id):
    cust = Customer.objects.get(id=id)
    bill_no=int(random.random()*100000)
    return render(request, 'bill.html', {'cust':cust, 'bill_no':bill_no})
    

@login_required
def delete_record(request, id):
    cust = Customer.objects.get(id=id)
    cust.delete()
    messages.success(request, "Customer Record Deleted" )
    return HttpResponseRedirect("/task")


@login_required
def month_date(request):
    now = datetime.today()
    one_month_ago = datetime(now.year, now.month - 1, now.day)
    month_end = datetime(now.year, now.month, now.day+1) - timedelta(seconds=1)
    cust = Customer.objects.filter(date__gt=one_month_ago,date__lt=month_end)
    month_earn=cust.aggregate(Sum('paid'))
    return month_earn['paid__sum']


@login_required
def today_date(request):
    now = datetime.today()
    today_morning = datetime(now.year, now.month, now.day)
    cust = Customer.objects.filter(date__gt=today_morning,date__lt=now)
    daily_earn=cust.aggregate(Sum('paid'))
    return daily_earn['paid__sum'] 

def bad_request(request, exception):
    return render(request, '404.html')