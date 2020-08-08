from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from devxpand.courses.models import Course
from django.conf import settings
from model_mommy import mommy

class CourseManagerTestCase(TestCase):
    
    def setUp(self):
        self.courses_django = mommy.make(
            'courses.Course', name='Python on the Web with Django', _quantity=10
        )
        self.courses_dev = mommy.make(
            'courses.Course', name='Python for Devs', _quantity=10
        )
        self.client = Client()
        
    def tearDown(self):
        Course.objects.all().delete()
        
    def test_course_search(self):
        search = Course.objects.search('django')
        self.assertEqual(len(search), 10)
        search = Course.objects.search('devs')
        self.assertEqual(len(search), 10)
        search = Course.objects.search('python')
        self.assertEqual(len(search), 20)