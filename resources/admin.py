from django.contrib import admin

# Register your models here.
from resources.models import Branch, Website, WebsiteImage, WebsiteExternalUrl, WebsiteExternalCard, WebsitePage

class WebsiteImageInline(admin.StackedInline):
    model = WebsiteImage

class WebsiteExternalUrlInline(admin.StackedInline):
    model = WebsiteExternalUrl

class WebsiteExternalCardInline(admin.StackedInline):
    model = WebsiteExternalCard

class WebsitePageInline(admin.StackedInline):
    model = WebsitePage

class WebsiteAdmin(admin.ModelAdmin):
    inlines = [
        WebsiteImageInline,
        WebsiteExternalUrlInline,
        WebsiteExternalCardInline,
        WebsitePageInline
    ]

admin.site.register(Branch) 
admin.site.register(Website, WebsiteAdmin)

