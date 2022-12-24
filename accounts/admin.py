from django.contrib import admin

# Register your models here.

from .models import Customer, Product, Order, Tag

class CustomerAdmin(admin.ModelAdmin):
  list_diplay = ['name', 'phone', 'email']
  search_fields = ['name']
  readonly_fields = ['date_created']

admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
  list_diplay = ['name', 'price', 'category']
  search_fields = ['name']
  readonly_fields = ['date_created']


admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
admin.site.register(Order)