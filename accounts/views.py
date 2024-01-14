from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .decorators import unauthenicated_user, allowed_users
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
# Create your views here.


@unauthenicated_user
def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@unauthenicated_user
def register_view(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            messages.success(request, f'{user} was created')
            return redirect('/login')
    return render(request, "accounts/registeration.html", {'form': form})


@login_required(login_url='login')
@allowed_users(['admin'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    totalOrders = orders.count()
    pending = orders.filter(status='Pending').count()
    delivered = orders.filter(status='Delivered').count()

    return render(request, 'accounts/dashboard.html', {'orders': orders, 'customers': customers, 'totalOrders': totalOrders, 'delivered': delivered, 'pending': pending})


@login_required(login_url='login')
@allowed_users(['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(['admin'])
def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    total_orders = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    return render(request, 'accounts/customer.html', {'customer': customer, 'orders': orders, 'total_orders': total_orders, 'myFilter': myFilter})


@login_required(login_url='login')
@allowed_users(['admin'])
def create_order(request, id):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=id)
    formSet = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        formSet = OrderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('/')

    return render(request, 'accounts/create_order.html', {'formSet': formSet})


@login_required(login_url='login')
@allowed_users(['admin'])
def update_order(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/create_order.html', {'form': form})


@login_required(login_url='login')
@allowed_users(['admin'])
def delete_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    return render(request, 'accounts/delete_order.html', {'order': order})
