import requests
import json
import sys

# Твой реальный URL (я уже настроил его)
BASE_URL = "https://w9vj84kyba.execute-api.us-east-1.amazonaws.com/Prod"

# Данные Пабло для загрузки
payload = {
    "name": "Pablo Emilio Escobar Gaviria",
    "normalized_name": "PABLO ESCOBAR",
    "source": "OFAC",
    "entity_type": "INDIVIDUAL",
    "country": "Colombia",
    "remarks": "Added via Cloud API v0.2"
}

print(f"🚀 Отправка данных на {BASE_URL}/ingest ...")

try:
    # Отправляем POST запрос
    response = requests.post(f"{BASE_URL}/ingest", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 201:
        print("\n✅ УСПЕХ! Пабло теперь в облачной базе.")
    else:
        print("\n❌ ОШИБКА. Что-то пошло не так.")

except Exception as e:
    print(f"\n💀 Критическая ошибка подключения: {e}")
    print("Убедись, что установил библиотеку: pip install requests")