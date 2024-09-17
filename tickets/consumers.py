# tickets/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_tickets()

    async def disconnect(self, close_code):
        pass

    async def send_tickets(self):
        query_params = {
            'sysparm_query': 'state!=7',  # Exclui tickets fechados
            'sysparm_limit': '10',  # Limita o número de resultados a 10
            'sysparm_sortby': 'sys_created_on',  # Ordena por data de criação
        }

        user_acess = os.getenv("USER_ACESS")
        password = os.getenv("PASSWORD")

        url = 'https://dev229526.service-now.com/api/now/table/incident'

        try:
            response = requests.get(url, auth=HTTPBasicAuth(user_acess, password), params=query_params)
            response.raise_for_status()  
            tickets = response.json().get('result', [])
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter tickets: {e}")
            tickets = []

        filtered_tickets = [
            {key: ticket[key] for key in ["number", "sys_id", "short_description", "urgency", "sys_updated_by", "sys_updated_on"]}
            for ticket in tickets
        ]

        await self.send(text_data=json.dumps({
            "tickets": filtered_tickets
        }))
