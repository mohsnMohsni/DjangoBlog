from django.contrib import admin
from .models import (
    Category, Post, PostSetting, Comment, CommentLike
)


class ChildrenItemInline(admin.TabularInline):
    model = Category
    fields = ('title', 'slug')
    extra = 1
    show_change_link = True


class PostItemInline(admin.TabularInline):
    model = Post
    fields = ('title',)
    show_change_link = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'parent',)
    search_fields = ('slug', 'title',)
    list_filter = ('parent',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 4
    inlines = [
        ChildrenItemInline,
        PostItemInline,
    ]


class PostSettingStackInline(admin.StackedInline):
    model = PostSetting


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'convert_create_date',
                    'convert_publish_date', 'draft', 'author', 'comment_count')
    search_fields = ('title', 'content',)
    list_filter = ('draft', 'category',)
    date_hierarchy = 'publish_time'
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    list_per_page = 4
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_confirmed',
                    'like_count', 'dis_like_count',)
    search_fields = ('content',)
    list_filter = ('author', 'is_confirmed',)
    list_editable = ('is_confirmed',)
    list_per_page = 6


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'condition')
    raw_id_fields = ('comment', 'author')
    actions = ['set_like', 'set_dislike']
    list_per_page = 10

    def set_like(self, request, queryset):
        queryset.update(condition=True)

    set_like.short_description = "Set like comment"

    def set_dislike(self, request, queryset):
        queryset.update(condition=False)

    set_dislike.short_description = "Set dislike comment"


admin.site.register(Category, CategoryAdmin)
