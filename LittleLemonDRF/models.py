from django.db import models

# Create your models here.

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()

    def __str__(self):
        return self.title
class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    def __str__(self):
        return self.user.username + " " + self.item.title + " " + str(self.quantity)
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    delvery_crew = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='delivery_crew', null=True)
    def __str__(self):
        return self.user.username + " " + self.item.title + " " + str(self.quantity) + " " + self.delvery_crew.username