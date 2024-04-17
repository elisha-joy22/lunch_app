from django.contrib import admin
from accounts.models import CustomUser

# Register your models here.


admin.site.register(CustomUser)






admin.site.site_header = 'Lunch Poll Admin'           # default: "Django Administration"
admin.site.index_title = 'Control Panel'              # default: "Site administration"
admin.site.site_title = 'Lunch Poll Admin'