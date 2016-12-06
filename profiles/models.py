from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save


# Create your models here.
class ProfileManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(ProfileManager, self).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
    ProfileModel = instance.__class__
    try:
        new_id = ProfileModel.objects.order_by("id").last().id + 1
    except:
        new_id = 1
    return "profile/%s/%s" %(new_id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=upload_location,
                               null=True,
                               blank=True)
    bio = models.TextField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    objects = ProfileManager()

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profile:detail", kwargs={"slug": self.slug})

    def get_markdown(self):
        bio = self.bio
        markdown_text = markdown(bio)
        return mark_safe(markdown_text)



def create_slug(instance, new_slug=None):
    slug = slugify(instance.user.username, allow_unicode=True)
    if new_slug is not None:
        slug = new_slug
    qs = Profile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_profile_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_profile_receiver, sender=Profile)
