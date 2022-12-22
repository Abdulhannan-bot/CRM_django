from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer

def customer_profolio(sender, instance, created, **kwargs):
  if created:
      Customer.objects.create(
        user = instance,
        name = instance.username,
      )
  group = Group.objects.get(name='customers')
  instance.groups.add(group)

post_save.connect(customer_profolio, sender=User)