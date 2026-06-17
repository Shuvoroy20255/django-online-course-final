from django.db import models
from django.utils import timezone

class Question(models.Model):
    # Relates each question to a specific lesson in the online course
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    grade = models.IntegerField(default=1)

    def _str_(self):
        return self.question_text

class Choice(models.Model):
    # Relates multiple choices to a single question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def _str_(self):
        return self.choice_text

class Submission(models.Model):
    # Relates a user's enrollment/attempt to their submitted answers
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    date_submitted = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"Submission by {self.enrollment} on {self.date_submitted}"
