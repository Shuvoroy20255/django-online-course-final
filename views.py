from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def submit(request, lesson_id):
    # Retrieve the lesson object or return a 404 error if it doesn't exist
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    
    if request.method == 'POST':
        # Retrieve the user's active course enrollment
        # Adjust the query parameters if your system handles enrollment tracking differently
        enrollment = Enrollment.objects.filter(user=request.user, course=lesson.course).first()
        
        if not enrollment:
            return render(request, 'onlinecourse/course_details_bootstrap.html', {
                'course': lesson.course,
                'error': 'You must be enrolled in this course to take the exam.'
            })
            
        # Create a new blank exam submission instance for this user enrollment
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Pull all questions associated with this lesson
        questions = lesson.question_set.all()
        
        # Loop through questions to find selected answer choices within the POST request payload
        for question in questions:
            input_name = f"question_{question.id}"
            # Multi-choice questions can send multiple choices back as a list
            selected_choice_ids = request.POST.getlist(input_name)
            
            for choice_id in selected_choice_ids:
                choice = get_object_or_404(Choice, pk=choice_id)
                submission.choices.add(choice)
                
        # Save the populated transaction relationships
        submission.save()
        
        # Redirect the client directly to the exam result interface with the new submission tracking key
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(lesson.id, submission.id)))
        
    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(lesson.course.id,)))

def show_exam_result(request, lesson_id, submission_id):
    # Fetch the lesson context and specific submission transaction
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    earned_score = 0
    
    # Evaluate every question in the exam
    for question in lesson.question_set.all():
        total_score += question.grade
        
        # Filter down all possible choices for this specific question
        all_choices = question.choice_set.all()
        correct_choices = all_choices.filter(is_correct=True)
        
        # Pull what choices the user submitted for this exact question item
        user_choices = submission.choices.filter(question=question)
        
        # Check if the user's selected choices match the exact correct choices dataset
        if set(user_choices) == set(correct_choices):
            earned_score += question.grade
            
    # Calculate the total percent score (avoiding division-by-zero risks)
    percentage = (earned_score / total_score) * 100 if total_score > 0 else 0
    passed = percentage >= 70 # Standard 70% threshold parameter
    
    context = {
        'lesson': lesson,
        'submission': submission,
        'earned_score': earned_score,
        'total_score': total_score,
        'percentage': round(percentage, 2),
        'passed': passed
    }
    
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)
