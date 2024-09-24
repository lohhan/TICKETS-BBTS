from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from .api import update_tickets

class MyAppConfig(AppConfig):
    name = 'tickets'

    def ready(self):
        # Agenda a atualização dos tickets a cada 60 segundos
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_tickets, 'interval', seconds=60)
        scheduler.start()
