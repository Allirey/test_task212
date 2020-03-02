from django.contrib import admin
from .models import Article, Comment


def approve(modeladmin, request, queryset):
    queryset.update(status=Article.Status.PUBLISHED)


def decline(modeladmin, request, queryset):
    queryset.update(status=Article.Status.DRAFT)


class CommentInline(admin.TabularInline):
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

    list_display = ['title', 'created', 'updated', 'status']
    actions = [approve, decline]
    list_filter = ('status','created', 'updated')
    search_fields = ('title',)
    ordering = ('created',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
