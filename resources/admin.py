from django.contrib import admin
from .models import Branch, Website, WebsiteImage, WebsiteContact, WebsiteUrl, WebsiteCard, WebsitePage


class BranchAdmin(admin.ModelAdmin):
    list_display = ['group', 'name']
    list_filter = ['group__name']


class WebsiteImageInline(admin.StackedInline):
    model = WebsiteImage
    extra = 0
    fields = ['name', 'file', 'sort', 'is_logo']


class WebsiteContactInline(admin.StackedInline):
    model = WebsiteContact
    extra = 0
    fields = ['platform', 'name', 'value']


class WebsiteUrlInline(admin.StackedInline):
    model = WebsiteUrl
    extra = 0
    fields = ['platform', 'name', 'value']


class WebsiteCardInline(admin.StackedInline):
    model = WebsiteCard
    extra = 0
    fields = ['platform', 'name', 'value']


class WebsitePageInline(admin.StackedInline):
    model = WebsitePage
    extra = 0
    fields = ['platform', 'name', 'value']


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['group', 'name', 'branch',]
    list_filter = ['group__name',]
    fieldsets = [
        (
            'НАСТРОЙКИ',
            {
                'classes': ['collapse'],
                'fields': ['group', 'branch', 'path', 'is_published',],
            },
        ),
        (
            'ИНФОРМАЦИЯ',
            {
                'classes': ['collapse',],
                'fields': ['name', 'city', 'address', 'schedule', 'description',],},
        ),
    ]
    inlines = [
        WebsiteImageInline,
        WebsiteContactInline,
        WebsiteUrlInline,
        WebsiteCardInline,
        # WebsitePageInline
    ]

admin.site.register(Branch, BranchAdmin) 
admin.site.register(Website, WebsiteAdmin)

