from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import BaseUserManager
from django.contrib import messages
from .models import *
from .forms import *

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ProfileUpdateForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt
import json


# Logging in the user
def login_view(request):  # Renamed function to avoid name conflict
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            useremail = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            redirect_to = request.GET.get('next', 'home')    
            user = authenticate(request, username=useremail, password=password)
            
            login(request, user)  # This now correctly uses Django's login
            if 'next' in request.POST:
                return redirect(redirect_to)
            return redirect('home')
    else:
        next_value = request.GET.get('next', "home")
        request.session['next_value'] = next_value
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = UsersCreationForm(request.POST)
        if form.is_valid():
            try:
                # Normalize email and check if it exists
                email = form.cleaned_data['email'].lower()
                
                # Check if user exists but email isn't verified
                existing_user = Users.objects.filter(email=email).first()
                if existing_user:
                    if existing_user.is_email_verified:
                        messages.error(request, 'An account with this email already exists.')
                        return redirect('signup')
                    else:
                        # Optionally: Resend verification email
                        messages.info(request, 'This email is registered but not verified. Please check your email.')
                        return redirect('login')
                
                # Create new user
                user = form.save(commit=False)
                user.email = email
                user.save()
                
                # Log the user in
                # login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('login')  # Replace with your home page
            
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                return redirect('signup')
    else:
        form = UsersCreationForm()
    
    return render(request, 'signup.html', {'form': form})



# INDEX VIEW
def home(request):
    books = Books.objects.all()
    context = {"books": books}
    return render(request, 'index.html', context)



def questions(request, id):
    context = {'idd':id}
    return render(request, 'questions.html', context)



# REVIEWS VIEW
def multiplayer(request):
    return render(request, 'multiplayer.html')



# PROFILE VIEW
def profile(request):
    return render(request, 'profile.html')



# SETTINGS VIEW
def settings(request):
    return render(request, 'settings.html')



# CONTACT VIEW
def contact(request):
    return render(request, 'contact.html')



# QUESTIONS VIEW
@login_required
def questions(request, book_id, question_id=None):
    # Get the book object
    book = get_object_or_404(Books, id=book_id)
    
    # Get all questions for this book
    all_questions = Questions.objects.filter(book=book).select_related('chapter', 'verse')
    
    # Get user's session data for this quiz
    session_key = f'quiz_{book_id}'
    quiz_session = request.session.get(session_key, {
        'answered_questions': {},
        'current_question_index': 0,
        'score': 0,
        'questions_order': []
    })
    
    # Initialize questions order if not set
    if not quiz_session['questions_order']:
        question_ids = list(all_questions.values_list('id', flat=True))
        random.shuffle(question_ids)  # Randomize question order
        quiz_session['questions_order'] = question_ids
        request.session[session_key] = quiz_session
        request.session.modified = True
    
    # Determine the current question
    if question_id:
        # If specific question is requested, find its index
        try:
            current_index = quiz_session['questions_order'].index(int(question_id))
        except ValueError:
            current_index = quiz_session['current_question_index']
    else:
        current_index = quiz_session['current_question_index']
    
    # Get the current question ID from the ordered list
    current_question_id = quiz_session['questions_order'][current_index]
    current_question = get_object_or_404(Questions, id=current_question_id)
    
    # Get options for the current question
    options = list(QuestionOptions.objects.filter(question=current_question).values_list('option', flat=True))
    random.shuffle(options)  # Randomize options
    
    # Prepare verse reference
    verse_reference = f"{book.name} {current_question.chapter.chapter_number}:{current_question.verse.verse_number}"
    
    # Prepare context
    context = {
        'book': book,
        'current_question': {
            'id': current_question.id,
            'question': current_question.question,
            'correct_answer': current_question.correct_answer,
            'options': options,
            'verse_reference': verse_reference,
            'verse_text': current_question.verse.text,
        },
        'chapter': current_question.chapter,
        'verse': current_question.verse.verse_number,
        'score': quiz_session['score'],
        'rank': get_rank(quiz_session['score']),
        'selected_answers': quiz_session['answered_questions'],
    }
    
    return render(request, 'questions.html', context)



# RANKING VIEW
def get_rank(score):
    # Simple ranking system based on score
    if score < 5:
        return "Beginner"
    elif score < 10:
        return "Intermediate"
    elif score < 15:
        return "Advanced"
    else:
        return "Expert"



# STORE ANSWERS VIEW
@csrf_exempt
@login_required
def store_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_text = data.get('question')
            answer = data.get('answer')
            
            # Find the question
            question = get_object_or_404(Questions, question=question_text)
            book_id = question.book.id
            
            # Get session data
            session_key = f'quiz_{book_id}'
            quiz_session = request.session.get(session_key, {})
            
            # Check if already answered
            if question_text not in quiz_session.get('answered_questions', {}):
                # Check if answer is correct
                is_correct = answer == question.correct_answer
                
                # Update session data
                quiz_session['answered_questions'][question_text] = answer
                if is_correct:
                    quiz_session['score'] = quiz_session.get('score', 0) + 1
                
                # Move to next question if available
                current_index = quiz_session.get('current_question_index', 0)
                if current_index + 1 < len(quiz_session.get('questions_order', [])):
                    quiz_session['current_question_index'] = current_index + 1
                
                request.session[session_key] = quiz_session
                request.session.modified = True
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



# GET VERSE VIEW
@csrf_exempt
@login_required
def get_verse(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book_id = data.get('book_id')
            chapter_id = data.get('chapter_id')
            verse = data.get('verse')
            
            # Get the verse text
            book = get_object_or_404(Books, id=book_id)
            chapter = get_object_or_404(Chapters, id=chapter_id, book=book)
            verse_obj = get_object_or_404(Verses, verse_number=verse, chapter=chapter)
            
            return JsonResponse({
                'success': True,
                'verse_text': verse_obj.text
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



@login_required
def reviews_list(request):
    reviews = Review.objects.all().prefetch_related('replies', 'replies__user')
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'review':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been posted!')
                return redirect('reviews')
        
        elif form_type == 'reply':
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, id=review_id)
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.user = request.user
                reply.review = review
                reply.save()
                messages.success(request, 'Your reply has been posted!')
                return redirect('reviews')
    
    else:
        review_form = ReviewForm()
        reply_form = ReplyForm()
    
    return render(request, 'reviews.html', {
        'reviews': reviews,
        'review_form': review_form,
        'reply_form': reply_form
    })



@login_required
def profile(request):
    # Sample data - replace with your actual data logic
    context = {
        'quizzes_taken': 42,
        'correct_answers': 378,
        'user_rank': "Gold",
        'badges': [
            {'name': 'Fast Learner', 'image': 'badges/fast-learner.png', 'description': 'Answered 10 questions correctly in a row'},
            {'name': 'Book Worm', 'image': 'badges/book-worm.png', 'description': 'Completed all quizzes in a book'},
            {'name': 'Early Bird', 'image': 'badges/early-bird.png', 'description': 'Played 5 quizzes before 8 AM'},
        ],
        'recent_activities': [
            {'type': 'quiz', 'description': 'Completed "Genesis" quiz with 85% score', 'timestamp': '2023-06-15 14:30'},
            {'type': 'badge', 'description': 'Earned "Book Worm" badge', 'timestamp': '2023-06-14 09:15'},
            {'type': 'quiz', 'description': 'Completed "Exodus" quiz with 92% score', 'timestamp': '2023-06-12 18:45'},
        ],
        'quiz_history': [
            {'book_name': 'Genesis', 'date': '2023-06-15', 'score': 85, 'time_taken': 142},
            {'book_name': 'Exodus', 'date': '2023-06-12', 'score': 92, 'time_taken': 156},
            {'book_name': 'Leviticus', 'date': '2023-06-10', 'score': 78, 'time_taken': 203},
        ]
    }
    return render(request, 'profile.html', context)



@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        messages.success(request, 'Profile picture updated successfully!')
    return redirect('profile')



@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserEditForm
from django.db.models import Count
from .models import Users, Review, Reply


def is_admin(user):
    return user.is_staff or user.is_superuser



@login_required
@user_passes_test(is_admin)
def dashboard_view(request):
    total_users = Users.objects.count()
    active_sessions = request.session.keys()  # This is a simple example
    
    context = {
        'total_users': total_users,
        'active_sessions': len(active_sessions),
        'users': Users.objects.all()[:5]  # Show first 5 users
    }
    return render(request, 'dashboard.html', context)



@login_required
@user_passes_test(is_admin)
def dashboard_view(request):
    total_users = Users.objects.count()
    active_sessions = request.session.keys()  # Simple implementation
    
    context = {
        'total_users': total_users,
        'active_sessions': len(active_sessions),
        'users': Users.objects.all().order_by('-date_created')[:5]
    }
    return render(request, 'dashboard.html', context)



@login_required
@user_passes_test(is_admin)
def user_management(request):
    users = Users.objects.all().order_by('-date_created')
    return render(request, 'user_management.html', {
        'users': users,
        'total_users': users.count()
    })



@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('user_management')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'edit_user.html', {
        'form': form,
        'user': user
    })



@login_required
@user_passes_test(is_admin)
def update_user(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
    return redirect('user_management')



@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
    return redirect('user_management')



@login_required
@user_passes_test(is_admin)
def reports_view(request):
    # Example reports data
    user_signups = Users.objects.extra(
        select={'day': 'date(date_created)'}
    ).values('day').annotate(count=Count('id')).order_by('-day')[:7]
    
    review_stats = {
        'total_reviews': Review.objects.count(),
        'total_replies': Reply.objects.count(),
        'recent_reviews': Review.objects.select_related('user').order_by('-created_at')[:5]
    }
    
    return render(request, 'reports.html', {
        'user_signups': user_signups,
        'review_stats': review_stats
    })



@login_required
@user_passes_test(is_admin)
def settings_view(request):
    return render(request, 'settings.html')



@login_required
@user_passes_test(is_admin)
def active_sessions_view(request):
    # This is a simple implementation - you might want to use django-user-sessions
    active_users = Users.objects.filter(is_active=True).order_by('-last_login')[:20]
    return render(request, 'active_sessions.html', {
        'active_users': active_users,
        'total_active': active_users.count()
    })



@login_required
@user_passes_test(is_admin)
def pending_reports_view(request):
    # Example pending reports - you might want to create a Report model
    pending_reports = [
        {'id': 1, 'type': 'Inappropriate Content', 'reported_by': 'user1', 'date': '2023-06-15'},
        {'id': 2, 'type': 'Spam', 'reported_by': 'user2', 'date': '2023-06-14'},
    ]
    return render(request, 'pending_reports.html', {
        'pending_reports': pending_reports,
        'total_pending': len(pending_reports)
    })



# VIEW FOR THE PARTNERS
@login_required
@user_passes_test(is_admin)
def partners_view(request):
    partners = Partner.objects.filter(is_active=True).order_by('-date_added')
    return render(request, 'partners.html', {
        'partners': partners,
        'total_partners': partners.count()
    })



@login_required
@user_passes_test(is_admin)
def add_partner(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        website = request.POST.get('website', '')
        description = request.POST.get('description', '')
        logo = request.FILES.get('logo')
        
        Partner.objects.create(
            name=name,
            website=website,
            description=description,
            logo=logo
        )
        messages.success(request, 'Partner added successfully!')
        return redirect('partners')
    
    return redirect('partners')



@login_required
@user_passes_test(is_admin)
def update_partner(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id)
    
    if request.method == 'POST':
        partner.name = request.POST.get('name')
        partner.website = request.POST.get('website', '')
        partner.description = request.POST.get('description', '')
        
        if 'logo' in request.FILES:
            partner.logo = request.FILES['logo']
        
        partner.save()
        messages.success(request, 'Partner updated successfully!')
    
    return redirect('partners')



@login_required
@user_passes_test(is_admin)
def delete_partner(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id)
    
    if request.method == 'POST':
        partner.delete()
        messages.success(request, 'Partner deleted successfully!')
    
    return redirect('partners')



def public_partners(request):
    partners = Partner.objects.filter(is_active=True).order_by('-date_added')
    return render(request, 'public_partners.html', {
        'partners': partners,
        'total_partners': partners.count()
    })