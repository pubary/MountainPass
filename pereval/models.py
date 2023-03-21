from django.db import models
from django.db.models.functions import Lower


class User(models.Model):
    email = models.EmailField(max_length=128, null=False, blank=False)
    fam = models.CharField('fam', max_length=128,)
    name = models.CharField('name', max_length=128,)
    otc = models.CharField('otc', max_length=128, blank=True)
    phone = models.CharField('phone', max_length=32,)

    class Meta:
        constraints = [models.UniqueConstraint(Lower('email'), name='unique_email')]


class Coords(models.Model):
    latitude = models.DecimalField(decimal_places=4, max_digits=7, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=4, max_digits=7, null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)


class Level(models.Model):
    winter = models.CharField(max_length=16, blank=True)
    spring = models.CharField(max_length=16, blank=True)
    summer = models.CharField(max_length=16, blank=True)
    autumn = models.CharField(max_length=16, blank=True)


class Added(models.Model):
    STATUS = [('new', 'new'), ('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected')]
    beauty_title = models.CharField(max_length=128, )
    title = models.CharField(max_length=128, )
    other_titles = models.CharField(max_length=128, )
    connect = models.CharField(max_length=128, blank=True)
    add_time = models.DateTimeField()
    send_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=STATUS, default='new',)
    coords = models.OneToOneField(Coords, blank=True, on_delete=models.SET_NULL, null=True)
    level = models.OneToOneField(Level, blank=True, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Images(models.Model):
    pereval = models.ForeignKey(Added, related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=64, )
    data = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, )
    added_date = models.DateTimeField(auto_now_add=True, )


