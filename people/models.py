from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass  #able to add your own custom feild here 



class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    


class Stock(models.Model):
    company_name = models.CharField(max_length=20)
    company_ticker = models.CharField(max_length=10)
    shares = models.FloatField()
    avg_share_price = models.FloatField()
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)  #an agent can have multiple stocks

    def __str__(self):
        amount_in = self.shares * self.avg_share_price
        return str(round(amount_in,2))


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Agent.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)