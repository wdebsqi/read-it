from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):
    databases = {"test"}
