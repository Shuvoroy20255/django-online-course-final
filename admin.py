from django.contrib import admin
# Importing exactly seven required classes/models from the local application
from .models import Course, Lesson, Enrollment, Question, Choice, Submission, QuestionInline

# 1. Define ChoiceInline to allow adding multiple choices to a question dynamically
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

# 2. Define QuestionInline to embed questions directly inside a Lesson view
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

# 3. Define QuestionAdmin configuration to link the ChoiceInline view
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'lesson', 'grade')
    search_fields = ['question_text']

# 4. Define LessonAdmin configuration to link the QuestionInline view
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course']

# Registering models with their corresponding admin interfaces
admin.site.register(Question, QuestionAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Choice)
admin.site.register(Submission)
