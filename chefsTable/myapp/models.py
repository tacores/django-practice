from django.db import models

# Create your models here.
class DrinksCategory(models.Model):
    category_name = models.CharField(max_length=200)

class Drinks(models.Model):
    drink_name = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.ForeignKey(DrinksCategory, on_delete=models.PROTECT, default=None)

class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    guest_count = models.IntegerField()
    reservation_time = models.DateField(auto_now=True) # auto_now=True の場合、フォーム上には表示されない
    comments = models.CharField(max_length=1000)

    def __str__(self):
        # admin画面でのデータ表示に使われる
        # より詳細に制御するには、admin.py で admin.ModelAdminを使ってカスタマイズする
        return f"{self.first_name} {self.last_name} ({self.guest_count}) {self.reservation_time}"
