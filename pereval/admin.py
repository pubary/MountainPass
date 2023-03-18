from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UsersCreationForm, UsersChangeForm
from .models import Users, Added, Tourist, Coords, Level, Images


class UsersAdmin(UserAdmin):
    add_form = UsersCreationForm
    form = UsersChangeForm
    model = Users
    list_display = ['email', 'username', 'first_name', 'last_name', 'fath_name']
    list_display_links = ('email', 'username',)


class AddedAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'coord_id', 'level_id', 'status', 'add_time')
    list_display_links = ('title',)


class CoordsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'height', 'latitude', 'longitude')
    list_display_links = ('pk', 'height',)


class LevelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'level_winter', 'level_spring', 'level_summer', 'level_autumn')
    list_display_links = ('pk',)


class TouristAdmin(admin.ModelAdmin):
    list_display = ('tourist', 'pereval')

admin.site.register(Users, UsersAdmin)
admin.site.register(Added, AddedAdmin)
admin.site.register(Tourist, TouristAdmin)
admin.site.register(Coords, CoordsAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Images)

