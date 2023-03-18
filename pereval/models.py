from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


class Users(AbstractUser):
    email = models.EmailField(
        "email address",
        primary_key=True,
        max_length=128,
        unique=True,
        null=False,
        blank=False
    )
    username = models.CharField(
        "login",
        max_length=128,
        unique=True,
        editable=True,
    )
    first_name = models.CharField('name', max_length=128,)
    last_name = models.CharField('fam', max_length=128, blank=True)
    fath_name = models.CharField('otc', max_length=128, blank=True)
    phone = models.CharField('phone', max_length=32,)

    class Meta(AbstractUser.Meta):
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='unique_email',
            ),
        ]


class Coords(models.Model):
    latitude = models.DecimalField(decimal_places=3, max_digits=4, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=3, max_digits=4, null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)


class Level(models.Model):
    level_winter = models.CharField(max_length=64, blank=True)
    level_spring = models.CharField(max_length=64, blank=True)
    level_summer = models.CharField(max_length=64, blank=True)
    level_autumn = models.CharField(max_length=64, blank=True)


class Added(models.Model):
    beauty_title = models.CharField(max_length=128, )
    title = models.CharField(max_length=128, )
    other_titles = models.CharField(max_length=128, )
    connect = models.CharField(max_length=128, )
    add_time = models.DateTimeField(auto_now_add=True, )
    status = models.CharField(max_length=16, default='new',)
    coord_id = models.OneToOneField(Coords, blank=True, on_delete=models.SET_NULL, null=True)
    level_id = models.OneToOneField(Level, blank=True, on_delete=models.SET_NULL, null=True)


class Images(models.Model):
    pereval = models.ForeignKey(Added, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, )
    foto = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, )
    added_date = models.DateTimeField(auto_now_add=True, )


class Tourist(models.Model):
    tourist = models.OneToOneField(Users, on_delete=models.CASCADE)
    pereval = models.ForeignKey(Added, on_delete=models.CASCADE)

