from django.contrib import admin

# Register your models here.
from .models import Group, Principal, AgentHistory, Membership, CustomUser, StartRest, EndRest


from django.contrib import admin



class EndRestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        ('Date information', {'fields': ['start_rest']}),
    ]

admin.site.register(EndRest, EndRestAdmin)


admin.site.register(Group)
admin.site.register(Principal)
admin.site.register(StartRest)
admin.site.register(AgentHistory)
admin.site.register(Membership)
admin.site.register(CustomUser)
