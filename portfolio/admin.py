from django.contrib import admin
from imagekit.admin import AdminThumbnail
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.utils.html import format_html

# Register your models here.
from .models import Photo, Site, Album, Frontpage, Portfolio

class PhotoInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Photo
    readonly_fields = ('__str__', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='photo_mini_thumb')

class AlbumAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline,
    ]
class FrontpageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')

    def admin_thumbnail(self, obj):
        return format_html('<img src="{}" style="width: 200px; \
                           height: auto"/>'.format(obj.image.photo_mini_thumb.url))

    admin_thumbnail.short_description = 'thumbnail'

class PortfolioAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')

    def admin_thumbnail(self, obj):
        return format_html('<img src="{}" style="width: 200px; \
                           height: auto"/>'.format(obj.image.photo_mini_thumb.url))

    admin_thumbnail.short_description = 'thumbnail'

admin.site.register(Album, AlbumAdmin)
admin.site.register(Site)
admin.site.register(Frontpage, FrontpageAdmin)
admin.site.register(Portfolio, PortfolioAdmin)