from django.shortcuts import render
from django.http import HttpResponse
from .models import *

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
    if id:
        return render(request, 'accounts/customer.html', {'customer': customer, 'orders': orders, 'total_orders': total_orders})
    return render(request, 'accounts/customer.html')
