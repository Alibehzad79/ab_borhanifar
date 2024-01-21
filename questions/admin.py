from django.contrib import admin
from questions.models import Question, Answer, QuestionPrice, QuestionTitle, QuestionComplete


# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['short_id', 'name', 'email', 'is_pay', 'date_sent']
    list_filter = ['is_pay', 'date_sent']
    list_editable = ['is_pay']
    search_fields = ['name', 'email']
    ordering = ['-date_sent']
    list_display_links = ['short_id', 'name']


@admin.register(QuestionComplete)
class QuestionComplete(admin.ModelAdmin):
    list_display = ['question_title', 'user', 'email', 'is_answered', 'date_created']
    list_filter = ['is_answered', 'date_created']
    list_editable = ['is_answered']
    inlines = [AnswerInline]
    search_fields = ['question_title', 'email']
    ordering = ['-date_created']


@admin.register(QuestionPrice)
class QuestionPriceAdmin(admin.ModelAdmin):
    list_display = ['price', 'q_count']
    list_editable = ['q_count']


admin.site.register(QuestionTitle)
