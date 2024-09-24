from ninja import NinjaAPI
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

api = NinjaAPI()

tickets_cache = []

load_dotenv()

def fetch_tickets():
    query_params = {
        'sysparm_query': 'state!=7',  
        'sysparm_limit': '10',  
        'sysparm_sortby': 'sys_created_on',  
        'sysparm_orderby': 'DESC'  
    }
    
    user_acess = os.getenv("USER_ACESS")
    password = os.getenv("PASSWORD")
    url = "https://dev282633.service-now.com/api/now/table/incident"
    
    response = requests.get(url, auth=HTTPBasicAuth(user_acess, password), params=query_params)
    tickets = response.json().get('result', [])

    base_url = "https://dev282633.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number="
    
    # Filtra e prepara os dados dos tickets
    filtered_tickets = [
        {
            **{key: ticket[key] for key in ["number", "sys_id", "short_description", "priority", "category", "sys_updated_by", "sys_updated_on", "sys_created_on"]},
            'link': f"{base_url}{ticket['number']}"  
        }
        for ticket in tickets
    ]

    return filtered_tickets

def update_tickets():
    global tickets_cache
    tickets_cache = fetch_tickets()
    print("Tickets atualizados com sucesso.")

scheduler = BackgroundScheduler()
scheduler.add_job(update_tickets, 'interval', seconds=60)
scheduler.start()

update_tickets()

@api.get("/tickets")
def get_tickets(request):
    return tickets_cache 
