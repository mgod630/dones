import asyncio, requests
from suds.client import Client

async def send_message_by_313(mobile , message):
    url = f'https://peyk313.ir/API/V1.0.0/Send.ashx?privatekey=6e2c5384-ee51-44b4-9fa4-711a2cd524d0&number=6600033&text={message}&isFlash=false&udh=""&mobiles={mobile}&clientIDs=1001'
    r = requests.get(url)
    return r.status_code
