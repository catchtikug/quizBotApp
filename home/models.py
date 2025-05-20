from django.db import models
from .managers import UsersManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model


# Model for storing Users
class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=150, unique=True)
    country = CountryField()
    profile_pic = CloudinaryField('ProfilePictures', null=True, blank=True)
    bio = models.TextField()
    user_agreement_accepted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = UsersManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_agreement_accepted', 'country']
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural = '1. Users'
    def image_tag(self):
        return mark_safe('<img width="100" height="100" src="%s"/>' %(self.profile_pic.url))
    

# Model for Categories
class Categories(models.Model):
    name = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '2. Categories'


# Model for Books
class Books(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '3. Books'


# Model for chapters
class Chapters(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    chapter_number = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        chapter_number = str(self.chapter_number)
        return chapter_number
    class Meta:
        verbose_name_plural = '4. Chapters'

    
# Model for verses
class Verses(models.Model):
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    verse_number = models.IntegerField(default=0)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        verse_number = str(self.verse_number)
        return verse_number
    class Meta:
        verbose_name_plural = '5. Verses'


# Model for Questions
class Questions(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE)
    verse = models.ForeignKey(Verses, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.question
    class Meta:
        verbose_name_plural = '6. Questions'


# Model for the options
class QuestionOptions(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    option = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.option
    class Meta:
        verbose_name_plural = '7. QuestionOptions'



User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username}"


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'replies'

    def __str__(self):
        return f"Reply by {self.user.username}"
    