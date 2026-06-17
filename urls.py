from django.urls import path
from . import views

# Defining the application namespace matching your previous template targets
app_name = 'onlinecourse'

urlpatterns = [
    # ... 
    # Keep your existing default paths here (e.g., course list, registration, login views)
    # ...

    # Path to handle quiz form submission processing
    path('lesson/<int:lesson_id>/submit/', views.submit, name='submit'),
    
    # Path to display the calculated scores and results after submission
    path('lesson/<int:lesson_id>/exam_result/<int:submission_id>/', views.show_exam_result, name='show_exam_result'),
]
