from django.contrib import admin

from myledger.models import MyGroup, Tally, Transaction

# Register your models here.
admin.site.register(MyGroup)
admin.site.register(Tally)
admin.site.register(Transaction)