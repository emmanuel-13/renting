from importlib.resources import contents
from time import timezone
from urllib import response
from django.test import TestCase
from customer.models import *


class customerModelClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Contact.objects.create(email="test@gmail.com", subject="Testing My Content", content="all the best for now and more of it")
        Subscribers.objects.create(email="test@gmail.com")
        MailMessage.objects.create(title="Rent4Less Automated Response", 
                                   content="all the best and thank you for subscribing for rent4less",
                                   )
        User.objects.create_user(username="test", password="test123", email="test123@gmail.com")
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass
    
    def test_detail_label_model(self):
        contact = Contact.objects.get(id=1)
        subscribers = Subscribers.objects.get(id=1)
        mail = MailMessage.objects.get(id=1)
        field_label = contact._meta.get_field('subject').verbose_name
        field_label2 = subscribers._meta.get_field('email').verbose_name
        field_label3 = mail._meta.get_field('title').verbose_name
        self.assertEqual(field_label, ('subject'))
        self.assertEqual(field_label2, ('email'))
        self.assertEqual(field_label3, ('title'))
        
    def test_detail_length_model(self):
        contact = Contact.objects.get(id=1)
        subscribers = Subscribers.objects.get(id=1)
        mail = MailMessage.objects.get(id=1)
        max_length_contact = contact._meta.get_field('subject').max_length
        max_length_subscriber = subscribers._meta.get_field('email').max_length
        max_length_mail = mail._meta.get_field('title').max_length
        self.assertEqual(max_length_contact, 50)
        self.assertEqual(max_length_subscriber, 254)
        self.assertEqual(max_length_mail, 200)

    # def setUp(self):
    #     print("setUp: Run once for every test method to setup clean data.")
    #     pass

    # def test_false_is_false(self):
    #     print("Method: test_false_is_false.")
    #     self.assertFalse(False)

    # def test_false_is_true(self):
    #     print("Method: test_false_is_true.")
    #     self.assertTrue(True)

class customerViewClass(TestCase):
    def setUpTestData(cls):
        
        contact_count = 3
        mail_count = 3
        
        for contact_id in range(contact_count):
            Contact.objects.create(
                email="test@gmail.com", subject="welcome here now", content="all the best for now"
            )
            
        for mail_id in range(mail_count):
            MailMessage.objects.create(
                title="welcome here now", content="all the best for now"
            )
            
        
        def test_view_url_exists_contact(self):
            response = self.client.get('/customer/contact/')
            self.assertEqual(response.status_code, 200)
            
        def test_view_url_reverse_contact(self):
            response = self.client.get(reverse('contact'))
            self.assertEqual(response.status_code, 200)
            
        def test_view_templates_contact(self):
            response = self.client.get(reverse('contact'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'contact.html')
            
        def test_view_url_exists_mail(self):
            response = self.client.get('/customer/mail/')
            self.assertEqual(response.status_code, 200)
            
        def test_view_url_reverse_mail(self):
            response = self.client.get(reverse('mail'))
            self.assertEqual(response.status_code, 200)
            
        def test_view_templates_mail(self):
            response = self.client.get(reverse('mail'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'contact.html')