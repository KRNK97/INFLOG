from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# we will add a picture field to the exisiting User model
# We will create a Profile model which will have a one to one relation with the User model an extra fields such as bio and picture...i.e one user will have his own single profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # default image name and dir where they will be uploaded
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # override the save method for the class so we can scale down the image and then save it
    # using pillow for resizing
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# signals to automatically create profile for each user

# create profile when user signs up
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('Profile created !')


# save profile when user signs up
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    print('Profile saved !')


# post_save.connect(create_profile, sender=User)
# post_save.connect(save_profile, sender=User)
