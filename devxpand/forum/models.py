from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager


class Thread(models.Model):
    
    title = models.CharField('Title', max_length=100)
    slug = models.SlugField('Identifier', max_length=100, unique=True)
    body = models.TextField('Message')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Author', on_delete=models.CASCADE, related_name='threads'
    )
    views = models.IntegerField('Views', blank=True, default=0)
    answers = models.IntegerField('Answers', blank=True, default=0)
    
    tags = TaggableManager()
    
    created = models.DateTimeField('Created at', auto_now_add=True)
    modified = models.DateTimeField('Modified at', auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse ('forum:thread', args=[self.slug])
    
    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['-modified']


class Reply(models.Model):
    
    thread = models.ForeignKey(
        Thread, verbose_name='Topic', on_delete=models.CASCADE, related_name='replies'
    )
    reply = models.TextField('Answer')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Author', on_delete=models.CASCADE, related_name='replies'
    )
    correct = models.BooleanField('Correct?', blank=True, default=False)
    
    created = models.DateTimeField('Created at', auto_now_add=True)
    modified = models.DateTimeField('Modified at', auto_now=True)
    
    def __str__(self):
        return self.reply[:100]
    
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ['-correct', 'created']
        
def post_save_reply(created, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()
    if instance.correct:
        instance.thread.replies.exclude(pk=instance.pk).update(
            correct=False
        )

def post_delete_reply(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()
    
models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)

models.signals.post_delete.connect(
    post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply'
)
