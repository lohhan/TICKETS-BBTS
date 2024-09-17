import json
from ninja import NinjaAPI
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

api = NinjaAPI()

load_dotenv()

def fetch_tickets():
    query_params = {
        'sysparm_query': 'state!=7',  # Exclui tickets fechados
        'sysparm_limit': '10',  # Limita o número de resultados a 10
        'sysparm_sortby': 'sys_created_on',  # Ordena por data de criação
    }
    
    user_acess = os.getenv("USER_ACESS")
    password = os.getenv("PASSWORD")
    url = "https://dev229526.service-now.com/api/now/table/incident"
    
    response = requests.get(url, auth=HTTPBasicAuth(user_acess, password), params=query_params)
    tickets = response.json().get('result', [])

    base_url = "https://dev229526.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number="

    
    # Filtra e prepara os dados dos tickets
    filtered_tickets = [
        {
            **{key: ticket[key] for key in ["number", "sys_id", "short_description", "urgency", "sys_updated_by", "sys_updated_on"]},
            'link': f"{base_url}{ticket['number']}"  
        }
        for ticket in tickets
    ]

    return filtered_tickets

# Endpoint RESTful para retornar tickets
@api.get("/tickets")
def get_tickets(request):
    tickets = fetch_tickets()
    return tickets

