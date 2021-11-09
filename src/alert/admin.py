from django.contrib import admin

# Register your models here.
from alert.models import Projects, Contributors, Issues, Comments


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    pass


@admin.register(Contributors)
class ContributorsAdmin(admin.ModelAdmin):
    pass


@admin.register(Issues)
class IssuesAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass