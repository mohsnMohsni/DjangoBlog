from django.contrib import admin
from . import models


class ChildrenItemInline(admin.TabularInline):
    model = models.Category
    fields = ('title', 'slug')
    extra = 1
    show_change_link = True


class PostItemInline(admin.TabularInline):
    model = models.Post
    fields = ('title',)
    show_change_link = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'parent',)
    search_fields = ('slug', 'title',)
    list_filter = ('parent',)
    inlines = [
        ChildrenItemInline,
        PostItemInline,
    ]


class PostSettingStackInline(admin.StackedInline):
    model = models.PostSetting


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'publish_time', 'draft', 'author',)
    search_fields = ('title', 'content',)
    list_filter = ('draft', 'category',)
    date_hierarchy = 'publish_time'
    inlines = [
        PostSettingStackInline,
    ]
    list_editable = ('draft',)
    actions = ['make_published', 'make_draft']

    def make_published(self, request, queryset):
        queryset.update(draft=False)

    make_published.short_description = "Exit selected from draft"

    def make_draft(self, request, queryset):
        queryset.update(draft=True)

    make_draft.short_description = "Join selected to draft"


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_confirmed', 'like_count', 'dis_like_count',)
    search_fields = ('content',)
    list_filter = ('author', 'is_confirmed',)


@admin.register(models.CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Category, CategoryAdmin)
