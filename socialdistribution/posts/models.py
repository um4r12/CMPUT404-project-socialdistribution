import uuid

from django.db import models
from profiles.models import Author
from profiles.utils import get_profile
from socialdistribution.utils import get_hostname
from django.utils import timezone


MARKDOWN = 'text/markdown'
PLAIN = 'text/plain'
BASE64 = 'application/base64'
PNG = 'image/png;base64'
JPEG = 'image/jpeg;base64'

CONTENT_TYPE_CHOICES = (
    (MARKDOWN, MARKDOWN),
    (PLAIN, PLAIN),
    (BASE64, BASE64),
    (PNG, PNG),
    (JPEG, JPEG),
)

'''
reference:
https://stackoverflow.com/questions/22340258/django-list-field-in-model
https://docs.djangoproject.com/en/3.0/howto/custom-model-fields/#converting-values-to-python-objects
'''
class ListField(models.TextField):

    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        '''converting-values-to-python-objects'''
        if not value:
            value = []

        if isinstance(value, list):
            #check the object is an instance of an list type
            return value

        return list(value.split(","))

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class Post(models.Model):
    PUBLIC = 'PUBLIC'
    FOAF = 'FOAF'
    FRIENDS = 'FRIENDS'
    PRIVATE = 'PRIVATE'
    SERVERONLY = 'SERVERONLY'
    # WEB = "WEB"
    # TUTORIAL = "TUTORIAL"

    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (FOAF, 'Friends of a friend'),
        (FRIENDS, 'Friends'),
        (PRIVATE, 'Private'),
        (SERVERONLY, 'Server only')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.CharField(blank=True, max_length=200)
    categories = models.CharField(blank=True, max_length=200)
    published = models.DateTimeField('date published', default=timezone.now)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES,
                                  default=PUBLIC)

    visibleTo = ListField(blank=True)
    unlisted = models.BooleanField(default=False)

    contentType = models.CharField(max_length=20,
                                   choices=CONTENT_TYPE_CHOICES,
                                   default=PLAIN)
    content = models.TextField(blank=True)

    @property
    def source(self):
        host = get_hostname()
        if host[-1] == "/":
            return("%sposts/%s" % (host, self.id))
        return("%s/posts/%s" % (host, self.id))

    @property
    def origin(self):
        host = get_hostname()
        if host[-1] == "/":
            return("%sposts/%s" % (host, self.id))
        return("%s/posts/%s" % (host, self.id))

    def categories_as_list(self):
        return self.categories.split(',')

    def serialize(self):

        fields = ["title", "source", "origin", "description", "content",
                  "contentType", "author", "categories", "comments",
                  "published", "id", "visibility", "visibleTo", "unlisted"]

        post = dict()
        for field in fields:
            if field == "author":
                post["author"] = self.author.serialize()
            elif field == "published":
                post["published"] = timezone.localtime(self.published)
            elif field == "categories":
                if self.categories != "":
                    post["categories"] = self.categories.split(',')
            elif field == "comments":
                comments = Comment.objects.filter(post=self).order_by("-published")
                post["comments"] = [comment.serialize() for comment in comments]
            # elif field == "visibleTo":
            #     post["visibleTo"] = self.visibleTo.to_python
            #     pass
            else:
                post[field] = str(getattr(self, field))

        return post


class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    published = models.DateTimeField('date published', auto_now_add=True)
    # published.editable=True
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    author = models.URLField(max_length=255)
    contentType = models.CharField(max_length=20,
                                   choices=CONTENT_TYPE_CHOICES,
                                   default=PLAIN)

    def serialize(self):

        fields = ["author", "comment", "contentType", "published",
                  "id"]
        comment = dict()
        for field in fields:
            if field == "author":
                comment["author"] = get_profile(self.author)
            elif field == "published":
                comment["published"] = timezone.localtime(self.published)
            else:
                comment[field] = str(getattr(self, field))

        return comment
