from django.test import TestCase

#Create your code here
class DemoTest(TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)  #right code
        #self.assertEqual(1 + 1, 3) #wrong code