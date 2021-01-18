from django.contrib import admin
from .models import FAQ, WhatWeDo
# Register your models here.

admin.site.register(FAQ)
class WhatWeDoAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(WhatWeDo, WhatWeDoAdmin)