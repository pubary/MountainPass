from django.contrib import admin
from .models import Users, Added, Coords, Level, Images


class UsersAdmin(admin.ModelAdmin):
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



admin.site.register(Users, UsersAdmin)
admin.site.register(Added, AddedAdmin)
admin.site.register(Coords, CoordsAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Images)

