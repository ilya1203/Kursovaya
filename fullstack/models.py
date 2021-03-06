from django.db import models

class Client(models.Model):
    login = models.CharField(max_length=255, verbose_name='Логин')
    psw = models.CharField(max_length=255, verbose_name='Пароль')

    def __str__(self):
        return self.login
    class Meta:
        ordering = ['login']

class Products(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.CharField(max_length=255, verbose_name='Цена')
    fromClient =  models.ForeignKey('Client', null=True, on_delete=models.PROTECT, verbose_name='Имя клиента')

    def __str__(self):
        return self.name

    def slf(self):
        return self

class Place(models.Model):
     place = models.CharField(max_length=255, verbose_name='Место')
     count = models.CharField(max_length=255, verbose_name='Количество')
     fromProduct = models.ForeignKey('Products', on_delete=models.PROTECT, verbose_name='Имя продукта')

     def __str__(self):
         return self.place

class Contacts_name(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя контакта')
    client = models.ForeignKey('Client', null=True, on_delete=models.PROTECT, verbose_name='Имя клиента')
    def __str__(self):
        return self.name
class Contacts_phone(models.Model):
    name = models.ForeignKey('Contacts_name', null=True, on_delete=models.PROTECT, verbose_name='Имя контакта')
    phone = models.CharField(max_length=255, verbose_name='Номер')
    def __str__(self):
        return self.phone
