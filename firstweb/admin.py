from django.contrib import admin
from django.contrib.auth.models import User
#from . import models

# Register your models here.

#admin.site.register(models.UserProfile)

from . models import CoffeehouseUser,Friend,Thread,ChatMessage

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread

class CoffeehouseUserAdmin(admin.ModelAdmin):
    search_fields=('username','email','college',)
    list_display=('username','email','college','image')

admin.site.register(CoffeehouseUser,CoffeehouseUserAdmin)
admin.site.register(Friend)
admin.site.register(Thread, ThreadAdmin)
