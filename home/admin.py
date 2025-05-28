from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin

# USERS ADMIN MODEL
class UsersAdmin(UserAdmin):
    add_form = UsersCreationForm
    form = UsersChangeForm
    model = Users
    list_display = ('id', 'email', 'username', 'country', 'date_created')
    list_filter = ()
    fieldsets = (
        ('None', {'fields': ('email', 'is_staff', 'is_active', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('country', 'user_agreement_accepted')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),)
    add_fieldsets = (
        ('None', {'fields': ('email', 'country', 'username', 'password')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),)
    search_fields = ('email', 'id')
    ordering = ['-date_created']
admin.site.register(Users, UsersAdmin)


# CATEGORIES ADMIN MODEL
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_created')
admin.site.register(Categories, CategoriesAdmin)


# BOOKS ADMIN MODEL
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'date_created')
admin.site.register(Books, BooksAdmin)


# CHAPTERS ADMIN MODEL
class ChaptersAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'chapter_number', 'date_created')
admin.site.register(Chapters, ChaptersAdmin)


# VERSES ADMIN MODEL
class VersesAdmin(admin.ModelAdmin):
    list_display = ('id', 'chapter', 'book', 'verse_number', 'text', 'date_created')
admin.site.register(Verses, VersesAdmin)


# QUESTIONS ADMIN MODEL
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'chapter', 'verse', 'question', 'correct_answer', 'date_created')
admin.site.register(Questions, QuestionsAdmin)


# QUESTION OPTIONS ADMIN MODEL
class QuestionOptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'option', 'date_created')
admin.site.register(QuestionOptions, QuestionOptionsAdmin)


# REVIEWS ADMIN MODEL
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'created_at', 'updated_at')
admin.site.register(Review, ReviewAdmin)


# REPLIES ADMIN MODEL
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'review', 'content', 'created_at', 'updated_at')
admin.site.register(Reply, ReplyAdmin)


# PATNERS ADMIN MODEL
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'is_active', 'date_added')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    
admin.site.register(Partner, PartnerAdmin)
