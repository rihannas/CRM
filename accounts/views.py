from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
# Create your views here.


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    totalOrders = orders.count()
    pending = orders.filter(status='Pending').count()
    delivered = orders.filter(status='Delivered').count()

    return render(request, 'accounts/dashboard.html', {'orders': orders, 'customers': customers, 'totalOrders': totalOrders, 'delivered': delivered, 'pending': pending})


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    total_orders = orders.count()

    return render(request, 'accounts/customer.html', {'customer': customer, 'orders': orders, 'total_orders': total_orders})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    form = OrderForm
    return render(request, 'accounts/create_order.html', {'form': form})


def update_order(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/create_order.html', {'form': form})
