from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator


from .models import *
from .forms import *
from .filters import *
from .decorators import *

# customer = Customer.objects.create(request.user, f'name - {i+1}', f'{1}'*10, f'{i}@gmail.com')
def generate(Customer, Order, Product):
  print('hello')
  # Customer.objects.delete()
  # for i in range(0,100):
  #   customer = Customer.objects.create(name = f'name - {i+1}', phone = f'{1}'*10, email = f'{i}@gmail.com')
  #   print(f'customer name = {customer.name}')
  #   # Customer.objects.create(customer)
  #   # product = Product.objects.create(name = f'product = {i+1}', price = i*100, category = 'Indoor', description = '-')
  #   orders = Order.objects.create(status =  'Pending')


@unauthenticated_user
def register_page(request):
  form = CreateUserForm()
  if(request.method == "POST"):
    form = CreateUserForm(request.POST)
    if form.is_valid:
      try:
        user = form.save()
      except:
        messages.error(request,f'Enter appropraite details')
        return redirect('register')
      username = form.cleaned_data.get('username')
      messages.success(request,f'Account was created for {username}')
      return redirect('login')
  context = {
    "form": form,
  }
  return render(request, 'accounts/register.html', context = context)


@unauthenticated_user
def login_page(request):
  if(request.method == 'POST'):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request,'Username or password is incorrect')
  context = {}
  return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
@admin_only
def home(request):
  
  customer_list = Customer.objects.all()

  my_filter_customer = CustomerFilter(request.GET, queryset = customer_list)
  customer_list = my_filter_customer.qs
  paginator_customer = Paginator(customer_list, 9)
  # print(f'paginator_customer {paginator_customer.objects_set.all()}')
  page_number_customer = request.GET.get('page_customer')
  print(f'page number {page_number_customer}')
  page_customer = paginator_customer.get_page(page_number_customer)

  orders = Order.objects.all()
  my_filter_order = OrderFilter(request.GET, queryset = orders)
  orders_list = my_filter_order.qs
  paginator_order = Paginator(orders_list, 9)
  page_number_order = request.GET.get('page_order')
  page_order = paginator_order.get_page(page_number_order)
  print(orders.count()/9)

  orders_count = orders_list.count()
  orders_delivered = orders_list.filter(status = "Delivered").count()
  orders_pending = orders_list.filter(status = "Pending").count()
  print(request.user)
  # for i in page.object_list:
  #   print(i.product)

  context = {
    "customers": customer_list,
    "orders": orders_list,
    "orders_count": orders_count,
    "orders_delivered": orders_delivered,
    "orders_pending": orders_pending,
    # "count": paginator.count,
    "page_customer": page_customer,
    "page_order": page_order,
    "my_filter_customer": my_filter_customer,
    "my_filter_order": my_filter_order,
  }
  return render(request, 'accounts/dashboard.html', context = context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customers'])
def user_page(request):
  orders = request.user.customer.order_set.all()
  orders_count = orders.count()
  orders_delivered = orders.filter(status = "Delivered").count()
  orders_pending = orders.filter(status = "Pending").count()
  context = {
    "orders": orders,
    "orders_count": orders_count,
    "orders_delivered": orders_delivered,
    "orders_pending": orders_pending,
  }
  return render(request, 'accounts/user.html', context = context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customers'])
def account_settings(request):
  customer = request.user.customer
  form = CustomerForm(instance=customer)
  if request.method == 'POST':
    form = CustomerForm(request.POST, request.FILES, instance=customer)
    print(request.FILES)
    print(customer.profile_pic.url)
    if form.is_valid:
      form.save()
    else:
      print(form.errors)
      print(form.is_bound())
  context = {
    "form": form,
  }
  return render(request, 'accounts/account-settings.html', context = context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admins'])
def products(request):
  products_list = Product.objects.all()
  my_filter_product = ProductFilter(request.GET, queryset = products_list)
  products_list = my_filter_product.qs
  paginator_product = Paginator(products_list, 9)
  
  page_number_product = request.GET.get('page_product')
  page_product = paginator_product.get_page(page_number_product)
  context = {
    "products": products_list,
    "my_filter_product": my_filter_product,
    "page_product": page_product,
  }
  return render(request, 'accounts/products.html', context = context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admins'])
def customers(request, id):
  customer = Customer.objects.get(id=id)
  orders = customer.order_set.all()
  my_filter = OrderFilter(request.GET, queryset = orders)
  orders = my_filter.qs
  orders_count = orders.count()
  context = {
    "customer": customer,
    "orders": orders,
    "orders_count": orders_count,
    "my_filter": my_filter,
  }
  return render(request, 'accounts/customers.html', context = context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admins'])
def create_order(request, id=id):
  OrderFormset = inlineformset_factory(Customer, Order, fields=('product','status'), extra=5)
  customer = Customer.objects.get(id = id)
  formset = OrderFormset(queryset = Order.objects.none(), instance=customer) 
  # form = OrderForm(initial={'customer':customer})
  if request.method == 'POST':
    formset = OrderFormset(request.POST, instance=customer)
    # form = OrderForm(request.POST)
    if formset.is_valid():
      formset.save()
      return redirect('/')
  context = {
    "formset": formset,
  }
  return render(request, 'accounts/create-order.html', context = context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admins'])
def update_customer(request, id=id):
  customer = Customer.objects.get(id=id)
  form = UpdateCustomerForm(instance=customer)
  if request.method == 'POST':
    form = UpdateCustomerForm(request.POST, instance=customer)
    if form.is_valid():
      form.save()
      return redirect('/')
  context = {
    "form": form,
    "is_form": True,
  }
  return render(request, 'accounts/create-order.html',context = context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admins'])
def update_order(request, id=id):
  order = Order.objects.get(id=id)
  form = OrderForm(instance=order)
  if request.method == 'POST':
    form = OrderForm(request.POST, instance=order)
    if form.is_valid():
      form.save()
      return redirect('/')
  context = {
    "form": form,
    "is_form": True,
  }
  return render(request, 'accounts/create-order.html',context = context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admins'])
def delete_order(request, id=id):
  order = Order.objects.get(id=id)
  if request.method == 'POST':
    order.delete()
    return redirect('/')
  context = {
    "item": order,
  }
  return render(request, 'accounts/delete.html', context = context)


def logout_trigger(request):
  logout(request)
  return redirect('login')
