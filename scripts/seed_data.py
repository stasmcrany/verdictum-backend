import requests
import json
import time

# --- КОНФИГУРАЦИЯ ---
# Вставь сюда свой URL (как в index.html), без /search или /ingest на конце
# Например: https://w9vj84kyba.execute-api.us-east-1.amazonaws.com/Prod
API_URL = "https://w9vj84kyba.execute-api.us-east-1.amazonaws.com/Prod" 

# Тестовые данные (Реальные люди из списков OFAC/EU)
DATA_TO_LOAD = [
    {"name": "Vladimir Putin", "source": "OFAC", "reason": "President of the Russian Federation"},
    {"name": "Sergey Lavrov", "source": "EU", "reason": "Minister of Foreign Affairs"},
    {"name": "Roman Abramovich", "source": "UK", "reason": "Oligarch"},
    {"name": "Osama bin Laden", "source": "UN", "reason": "Historical Terrorist"},
    {"name": "Alisher Usmanov", "source": "OFAC", "reason": "Oligarch"},
    {"name": "Kim Jong Un", "source": "OFAC", "reason": "Supreme Leader of North Korea"}
]

def seed_database():
    print(f"🚀 Начинаем загрузку данных в: {API_URL}")
    print("-" * 40)

    endpoint = f"{API_URL}/ingest"
    
    success_count = 0
    
    for entity in DATA_TO_LOAD:
        print(f"Загружаю: {entity['name']}...", end=" ")
        
        try:
            # Отправляем POST запрос (как будто это делает админка)
            response = requests.post(endpoint, json=entity)
            
            if response.status_code == 201:
                print("✅ OK")
                success_count += 1
            else:
                print(f"❌ Ошибка {response.status_code}: {response.text}")
        except Exception as e:
            print(f"❌ Critical Error: {e}")

    print("-" * 40)
    print(f"🏁 Загрузка завершена. Успешно: {success_count}/{len(DATA_TO_LOAD)}")

if __name__ == "__main__":
    if "execute-api" not in API_URL:
        print("⚠️ ОШИБКА: Ты забыл вставить свой API_URL в скрипт!")
    else:
        seed_database()