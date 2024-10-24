from django.contrib import admin
from .models import User, WasteContainer, WasteType, Transaction

admin.site.register(User)
admin.site.register(WasteContainer)
admin.site.register(WasteType)
admin.site.register(Transaction)
