from django.contrib import admin

from .models import Voice, Indicators, TeamLeader, Leader, Agent, QcOperator, SetPolicy

admin.site.register(Voice)
admin.site.register(Indicators)
admin.site.register(TeamLeader)
admin.site.register(Leader)
admin.site.register(Agent)
admin.site.register(QcOperator)
admin.site.register(SetPolicy)


