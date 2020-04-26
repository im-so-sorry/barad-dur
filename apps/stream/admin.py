from django.contrib import admin

from apps.stream.models import Rule, Stream


class RuleInline(admin.TabularInline):
    model = Rule


# @admin.register(Stream)
# class StreamAdmin(admin.ModelAdmin):
#     inlines = [RuleInline]

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    pass
