from django.contrib import admin
from .models import User, Added, Tourist, Coords, Level, Images


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'fam', 'name', 'otc']
    list_display_links = ('email', 'fam',)


class AddedAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'coords', 'level', 'status', 'add_time')
    list_display_links = ('title',)


class CoordsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'height', 'latitude', 'longitude')
    list_display_links = ('pk', 'height',)


class LevelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'winter', 'spring', 'summer', 'autumn')
    list_display_links = ('pk',)


class TouristAdmin(admin.ModelAdmin):
    list_display = ('tourist', 'pereval')

admin.site.register(User, UserAdmin)
admin.site.register(Added, AddedAdmin)
admin.site.register(Tourist, TouristAdmin)
admin.site.register(Coords, CoordsAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Images)

