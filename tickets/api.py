from ninja import NinjaAPI
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

api = NinjaAPI() # inicializando a api

tickets_cache = [] # criando uma lista de cache

load_dotenv() # carregando as credenciais do .env

def fetch_service_now(): 
    query_params = {
        'sysparm_query': 'state!=7^state!=8^state!=9',  
        'sysparm_sortby': 'sys_created_on',  
        'sysparm_orderby': 'DESC'  
    } # parametros de pesquisa
    
    # autenticação de acesso no service now
    user_acess = os.getenv("USER_ACESS")
    password = os.getenv("PASSWORD")
    url = "https://dev282633.service-now.com/api/now/table/incident"
    
    response = requests.get(url, auth=HTTPBasicAuth(user_acess, password), params=query_params)
    tickets = response.json().get('result', []) # coleto a resposta da api do service now e atribuo a uma variavel no formato json

    base_url = "https://dev282633.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number=" # base de url pra acessar o link do ticket em especifico
    
    # Filtra e prepara os dados dos tickets
    filtered_tickets = [
        {
            **{key: ticket[key] for key in ["number", "sys_id", "short_description", "priority", "category", "sys_updated_by", "sys_updated_on", "sys_created_on"]},
            'link': f"{base_url}{ticket['number']}"  
        }
        for ticket in tickets
    ]

    return filtered_tickets

def fetch_tickets(): 
    global tickets_cache
    tickets_cache = [] 
    tickets_cache += fetch_service_now()

# atualiza os tickets a cada 60s
def update_tickets(): 
    fetch_tickets()
    print("Tickets atualizados com sucesso.")

scheduler = BackgroundScheduler()
scheduler.add_job(update_tickets, 'interval', seconds=60)
scheduler.start()

update_tickets()

# rota da api 
@api.get("/tickets")
def get_tickets(request):
    return tickets_cache 