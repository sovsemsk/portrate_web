from django.contrib import admin
from .models import LinkIntegration, IikoIntegration, Bitrix24Integration, YclientsIntegration, TopnlabIntegration

admin.site.register(LinkIntegration) 
admin.site.register(IikoIntegration)
admin.site.register(Bitrix24Integration)
admin.site.register(YclientsIntegration)
admin.site.register(TopnlabIntegration)