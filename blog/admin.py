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
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 4
    inlines = [
        ChildrenItemInline,
        PostItemInline,
    ]


class PostSettingStackInline(admin.StackedInline):
    model = models.PostSetting


@admin.register(models.Post)
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
    actions = ['make_published', 'make_draft', 'allow_discoussion']

    # def allow_discoussion(self, request, queryset):
    #     models.PostSetting.objects.create(
    #         post=self, comment=False, author=False, postsetting__allow_discusstion=True)

    allow_discoussion.short_description = "allow user write comment on posts"

    def make_published(self, request, queryset):
        queryset.update(draft=False)

    make_published.short_description = "Exit selected from draft"

    def make_draft(self, request, queryset):
        queryset.update(draft=True)

    make_draft.short_description = "Join selected to draft"


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_confirmed',
                    'like_count', 'dis_like_count',)
    search_fields = ('content',)
    list_filter = ('author', 'is_confirmed',)
    list_editable = ('is_confirmed',)
    list_per_page = 6


@admin.register(models.CommentLike)
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


admin.site.register(models.Category, CategoryAdmin)
