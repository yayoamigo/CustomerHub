from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(default="", blank=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True )
    phone_number = models.CharField(max_length=20, default="", blank=True)
    email = models.EmailField(default="", blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")
    converted_date = models.DateTimeField(null=True, blank=True)

    objects = LeadManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def handle_upload_follow_ups(instance, filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"

    
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent')
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='agents')

    def __str__(self):
        return self.user.email

class Category(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
def handle_upload_follow_ups(instance, filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"

    
class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, related_name="followups", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.last_name}"
    
def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
