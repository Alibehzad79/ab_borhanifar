from django.contrib import admin
from questions.models import Question, Answer


# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['short_id', 'name', 'email', 'is_done', 'date_sent']
    list_filter = ['is_done', 'date_sent']
    list_editable = ['is_done']
    inlines = [AnswerInline]
    search_fields = ['name', 'email']
    ordering = ['-date_sent']
    list_display_links = ['short_id', 'name']
