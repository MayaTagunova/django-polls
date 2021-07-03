from django.contrib import admin
from .models import Choice, Question, Poll


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


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ['question_text']
    show_change_link = True


class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'pub_date']
    list_filter = ['pub_date']
    inlines = [QuestionInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Poll, PollAdmin)