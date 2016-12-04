from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.conf import settings
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class PortfolioManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PortfolioManager, self).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
    PortfolioModel = instance.__class__
    try:
        new_id = PortfolioModel.objects.order_by("id").last().id + 1
    except:
        new_id = 1
    return "portfolio/%s/%s" %(new_id, filename)

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    title = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    register = models.DateTimeField(auto_now=True, auto_now_add=False)
    category = models.ForeignKey(Category)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True)
    score = GenericRelation(Rating, related_query_name='portfolio')
    slug = models.SlugField(unique=True, allow_unicode=True)
    objects = PortfolioManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-register"]

    def get_absolute_url(self):
        return reverse("portfolio:detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("portfolio:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("portfolio:delete", kwargs={"slug": self.slug})


    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type




def create_slug(instance, new_slug=None):
    slug = slugify(instance.title, allow_unicode=True)
    if new_slug is not None:
        slug = new_slug
    qs = Portfolio.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_portfolio_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_portfolio_receiver, sender=Portfolio)