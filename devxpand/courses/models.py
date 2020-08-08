from django.db import models
from django.conf import settings
from django.utils import timezone
from devxpand.core.mail import send_mail_template

class CourseManager(models.Manager):
    
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )

class Course(models.Model):
    
    name = models.CharField('Name', max_length=100)
    slug = models.SlugField('Shortcut')
    description = models.TextField('Description', blank=True)
    about = models.TextField('About', blank=True)
    start_date = models.DateField('Start Date', null=True, blank=True)
    image = models.ImageField(upload_to='courses/images', verbose_name='Image', null=True, blank=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    
    objects=CourseManager()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('courses:details', args=[self.slug])
    
    def release_lessons(self):
        today = timezone.now().date()
        return self.lessons.filter(release_date__gte=today)
    
    class Meta:
        verbose_name='Course'
        verbose_name_plural='Courses'
        ordering=['Name']
        
class Lesson(models.Model):
    
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description', blank=True)
    number = models.IntegerField('Number (order)', blank=True, default=0)
    release_date = models.DateField('Release Date', blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name='Course', on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Update at', auto_now=True)
    
    def __str__(self):
        return self.name
    
    def is_available(self):
        if self.release_date:
            today = timezone.now().date()
            return self.release_date >= today
        return False
    
    class Meta:
        verbose_name = 'Lecture'
        verbose_name_plural = 'Lectures'
        ordering = ['number']
        
class Material(models.Model):
    
    name = models.CharField('Name', max_length=100)
    embedded = models.TextField('Video embedded', blank=True)
    file = models.FileField(upload_to='lessons/materials', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, verbose_name = 'Lecture', on_delete=models.CASCADE, related_name='materials')
    
    def is_embedded(self):
        return bool(self.embedded)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'
        

class Enrollment(models.Model):
    
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Canceled'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='User',
        on_delete=models.CASCADE, related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, verbose_name='Course', on_delete=models.CASCADE, related_name='enrollments'
    )
    status = models.IntegerField(
        'Status', choices=STATUS_CHOICES, default=1, blank=True
    )
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    
    def active(self):
        self.status = 1
        self.save()
        
    def is_approved(self):
        return self.status == 1
    
    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        unique_together = (('user', 'course'),)

class Announcement(models.Model):
    
    course = models.ForeignKey(
        Course, verbose_name='Course', on_delete=models.CASCADE, related_name='announcements'
    )
    title = models.CharField('Title', max_length=100)
    content = models.TextField('Content')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-created_at']
        
class Comment(models.Model):
    
    announcement = models.ForeignKey(
        Announcement, verbose_name='Announcement', on_delete=models.CASCADE, related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE
    )
    comment = models.TextField('Coment')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Update at', auto_now=True)

    class Meta:
        verbose_name = 'Coment'
        verbose_name_plural = 'Coments'
        ordering = ['created_at']
        
def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
         'announcement': instance   
        }
        template_name = 'courses/announcement_mail.html'
        enrollments = Enrollment.objects.filter(
            course = instance.course,
            status = 1
        )
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)
        
models.signals.post_save.connect(
    post_save_announcement, sender=Announcement, dispatch_uid='post_save_announcement'
)
