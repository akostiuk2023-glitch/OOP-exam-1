import os
import random
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Використовуємо правильний імпорт, який ми раніше налаштували
from google.adk import Agent

load_dotenv()

# ==========================================
# 1. АБСТРАКЦІЯ
# ==========================================
class Sensor(ABC):
    def __init__(self, name: str, unit: str):
        self.name = name
        self.unit = unit

    @abstractmethod
    def read(self):
        """Абстрактний метод для зчитування показників"""
        pass

# ==========================================
# 2. НАСЛІДУВАННЯ
# ==========================================
class TemperatureSensor(Sensor):
    def __init__(self):
        super().__init__(name="Термометр", unit="°C")

    # ==========================================
    # 4. ПОЛІМОРФІЗМ (реалізація абстрактного методу)
    # ==========================================
    def read(self) -> int:
        return random.randint(-10, 35) # Випадкова температура від -10 до +35

class HumiditySensor(Sensor):
    def __init__(self):
        super().__init__(name="Гігрометр", unit="%")

    # ПОЛІМОРФІЗМ
    def read(self) -> int:
        return random.randint(30, 100) # Випадкова вологість від 30% до 100%

# ==========================================
# КЛАС МЕТЕОСТАНЦІЇ
# ==========================================
class WeatherStation:
    def __init__(self, city: str):
        self.city = city
        # ==========================================
        # 3. ІНКАПСУЛЯЦІЯ (приватний атрибут)
        # ==========================================
        self.__sensors = []

    def add_sensor(self, sensor: Sensor):
        """Безпечне додавання датчика до приватного списку"""
        self.__sensors.append(sensor)

    def report(self) -> dict:
        """Збирає дані з усіх датчиків (демонстрація поліморфізму)"""
        temp = 0
        humidity = 0
        
        for sensor in self.__sensors:
            val = sensor.read() # Поліморфний виклик: кожен датчик повертає своє значення
            if sensor.unit == "°C":
                temp = val
            elif sensor.unit == "%":
                humidity = val
                
        # Проста логіка визначення погодних умов
        if humidity > 85:
            condition = "Дощ"
        elif temp > 20 and humidity < 60:
            condition = "Сонячно"
        else:
            condition = "Хмарно"

        return {
            "city": self.city,
            "temperature_c": temp,
            "humidity_percent": humidity,
            "condition": condition
        }

# ==========================================
# ІНСТРУМЕНТ ДЛЯ АГЕНТА
# ==========================================
def get_weather(city: str) -> dict:
    """Отримує дані про поточну погоду в заданому місті."""
    station = WeatherStation(city)
    station.add_sensor(TemperatureSensor())
    station.add_sensor(HumiditySensor())
    
    return station.report()

# ==========================================
# НАЛАШТУВАННЯ АГЕНТА
# ==========================================
agent_prompt = """Ти — метеорологічний помічник. 
Твоє завдання:
1. Використовувати інструмент get_weather, щоб дізнатися погоду в місті, яке називає користувач.
2. Повідомляти температуру, вологість та погодні умови.
3. На основі цих даних давати короткі рекомендації (наприклад: що вдягнути, чи брати парасолю).
Відповідай виключно українською мовою."""

root_agent = Agent(
    name="WeatherAgent",
    instruction=agent_prompt,
    tools=[get_weather]
)