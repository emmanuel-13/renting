from email.mime import base
from django.conf import settings
import requests


class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        path = f"/transaction/verify/{ref}"

        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json',
        }

        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']
    
    def list_payment(self, *args, **kwargs):
        path = f"/transaction"
        
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json',
        }
        
        url = self.base_url + path
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']
    
    def fetch_transaction(self, id, *args, **kwargs):
        
        path = f"/transaction/{id}"
        
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json',
        }
        
        url = self.base_url + path
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']
        
        
        