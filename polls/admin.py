from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
#        ('Date information', {'fields': ['pub_date']}),
        ('Type', {'fields': ['type']})
    ]

    list_display = ['question_text']
    list_filter = ['question_text']
    search_fields = ['question_text']
    inlines = [ChoiceInline]


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['pub_date']
        else:
            return []

admin.site.register(Question, QuestionAdmin)
