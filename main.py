from accounts.models import *

# returns all customers from customer table
customers = Customer.objects.all()

# returns first customer in table
firstCustomer = Customer.objects.first()

# returns last customer in table
lastCustomer = Customer.objects.last()

# returns single customer by name
customerByName = Customer.objects.get(name='Suga')

# returns single customer by id
customerById = Customer.objects.get(id=1)

# returns all orders related to a customer (firstCustomer)
orders = firstCustomer.order_set.all()

# returns who made the order  (querying the parent model aka referenced)
order = Order.objects.first()
customerName = order.customer.name

# returns products from products table with value of outdoor
produts = Product.objects.filter(category="out door")

# sort objects by id
leastToGreatest = Product.objects.all().order_by('id')
greatestToLeast = Product.objects.all().order_by('-id')

# returns all products with tag of "kitchen"
# tag__name means going to the tag model and then search by the name attribute
produtsFiltered = Product.objects.filter(tag__name="kitchen")
