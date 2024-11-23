import os
from abc import ABC, abstractmethod
from datetime import time
from typing import Dict

# Реалізація шаблону Singleton
class Singleton:
    """Базовий клас для реалізації шаблону Одинак"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance


# Менеджер налаштувань Singleton
class SettingsManager(Singleton):
    """Клас для керування налаштуваннями системи"""
    def __init__(self):
        if not hasattr(self, 'initialized'):
            # Словник з налаштуваннями за замовчуванням
            self.settings: Dict = {
                'default_temperature': 72,  # Температура за замовчуванням
                'default_brightness': 50,   # Яскравість за замовчуванням
                'security_armed': False     # Статус системи безпеки
            }
            self.initialized = True

    def get_setting(self, key: str):
        """Отримати значення налаштування за ключем"""
        return self.settings.get(key)

    def update_setting(self, key: str, value):
        """Оновити значення налаштування"""
        self.settings[key] = value


# Менеджер енергоспоживання Singleton
class EnergyManager(Singleton):
    """Клас для моніторингу та оптимізації енергоспоживання"""
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.total_consumption = 0          # Загальне споживання енергії
            self.active_devices = set()         # Множина активних пристроїв
            self.initialized = True

    def monitor_usage(self):
        """Моніторинг поточного споживання енергії"""
        return f"Current energy usage: {self.total_consumption}W"

    def optimize_energy(self):
        """Оптимізація енергоспоживання"""
        # Тут має бути логіка оптимізації енергоспоживання
        pass


# Підсистеми
class LightingSystem:
    """Підсистема керування освітленням"""
    def __init__(self):
        self.brightness = 0      # Поточна яскравість
        self.is_on = False      # Статус увімкнення

    def turn_on_lights(self):
        """Увімкнення світла"""
        self.is_on = True
        self.brightness = SettingsManager().get_setting('default_brightness')
        return "Lights turned on"

    def turn_off_lights(self):
        """Вимкнення світла"""
        self.is_on = False
        self.brightness = 0
        return "Lights turned off"

    def set_brightness(self, level: int):
        """Встановлення рівня яскравості"""
        if 0 <= level <= 100:
            self.brightness = level
            return f"Brightness set to {level}%"
        return "Invalid brightness level"


class SecuritySystem:
    """Підсистема безпеки"""
    def __init__(self):
        self.armed = False          # Статус охорони
        self.alarm_active = False   # Статус тривоги

    def arm_system(self):
        """Активація системи безпеки"""
        self.armed = True
        return "Security system armed"

    def disarm_system(self):
        """Деактивація системи безпеки"""
        self.armed = False
        self.alarm_active = False
        return "Security system disarmed"

    def trigger_alarm(self):
        """Активація тривоги"""
        if self.armed:
            self.alarm_active = True
            return "ALARM TRIGGERED!"
        return "System is not armed"


# Реалізація шаблону Міст (Bridge)
class Device(ABC):
    """Абстрактний клас для пристроїв"""
    @abstractmethod
    def start(self):
        """Запуск пристрою"""
        pass

    @abstractmethod
    def stop(self):
        """Зупинка пристрою"""
        pass


class RemoteControl(ABC):
    """Абстрактний клас для пультів керування"""
    def __init__(self, device: Device):
        self.device = device

    @abstractmethod
    def turn_on(self):
        """Увімкнення пристрою"""
        pass

    @abstractmethod
    def turn_off(self):
        """Вимкнення пристрою"""
        pass


# Конкретні пристрої
class TV(Device):
    """Клас для телевізора"""
    def start(self):
        return "TV started"

    def stop(self):
        return "TV stopped"


class AirConditioner(Device):
    """Клас для кондиціонера"""
    def start(self):
        return "AC started"

    def stop(self):
        return "AC stopped"


# Конкретні пульти керування
class TVRemote(RemoteControl):
    """Пульт керування телевізором"""
    def turn_on(self):
        return self.device.start()

    def turn_off(self):
        return self.device.stop()


class ACRemote(RemoteControl):
    """Пульт керування кондиціонером"""
    def turn_on(self):
        return self.device.start()

    def turn_off(self):
        return self.device.stop()


# Реалізація шаблону Фасад
class SmartHomeFacade:
    """Головний клас системи розумного дому"""
    def __init__(self):
        # Ініціалізація всіх підсистем
        self.lighting = LightingSystem()
        self.security = SecuritySystem()
        self.settings = SettingsManager()
        self.energy = EnergyManager()

        # Інтеграція шаблону Міст
        self.tv = TV()
        self.ac = AirConditioner()
        self.tv_remote = TVRemote(self.tv)
        self.ac_remote = ACRemote(self.ac)

    def activate_security_system(self):
        """Активація системи безпеки"""
        return self.security.arm_system()

    def deactivate_security_system(self):
        """Деактивація системи безпеки"""
        return self.security.disarm_system()

    def control_lighting(self, command: str, brightness: int = None):
        """Керування освітленням"""
        if command == "ON":
            return self.lighting.turn_on_lights()
        elif command == "OFF":
            return self.lighting.turn_off_lights()
        elif command == "ADJUST" and brightness is not None:
            return self.lighting.set_brightness(brightness)

    def control_entertainment(self, device: str, command: str):
        """Керування розважальними пристроями"""
        if device == "TV":
            if command == "ON":
                return self.tv_remote.turn_on()
            elif command == "OFF":
                return self.tv_remote.turn_off()
        return "Invalid command"

    def control_climate(self, command: str):
        """Керування кліматом"""
        if command == "ON":
            return self.ac_remote.turn_on()
        elif command == "OFF":
            return self.ac_remote.turn_off()
        return "Invalid command"


# Інтеграція голосового керування
class VoiceControl:
    """Клас для обробки голосових команд"""
    def __init__(self, smart_home: SmartHomeFacade):
        self.smart_home = smart_home

    def process_command(self, command: str):
        """Обробка голосових команд"""
        command = command.lower()
        if "light" in command:
            if "on" in command:
                return self.smart_home.control_lighting("ON")
            elif "off" in command:
                return self.smart_home.control_lighting("OFF")
        elif "security" in command:
            if "activate" in command:
                return self.smart_home.activate_security_system()
            elif "deactivate" in command:
                return self.smart_home.deactivate_security_system()
        return "Command not recognized"


def test_smart_home():
    """Функція для тестування системи розумного дому"""
    # Створення екземпляра системи
    smart_home = SmartHomeFacade()
    voice_control = VoiceControl(smart_home)

    # Тестування різних функцій
    tests = [
        smart_home.control_lighting("ON"),
        smart_home.control_lighting("ADJUST", 75),
        smart_home.activate_security_system(),
        smart_home.control_entertainment("TV", "ON"),
        smart_home.control_climate("ON"),
        voice_control.process_command("turn on lights"),
        voice_control.process_command("activate security")
    ]

    # Виведення результатів тестів
    for i, result in enumerate(tests, 1):
        print(f"Test {i}: {result}")

def clear_console():
    """Очищення консолі для різних операційних систем"""
    try:
        if os.name == 'nt':  # для Windows
            os.system('cls')
        else:  # для Unix/Linux/MacOS
            # Використовуємо print з escape-послідовністю замість os.system
            print('\033[2J\033[H', end='')
    except Exception:
        # Якщо очищення не спрацювало, просто додаємо порожні рядки
        print('\n' * 100)


def display_menu():
    """Відображення головного меню"""
    print("\n=== СИСТЕМА РОЗУМНОГО ДОМУ ===")
    print("1. Керування освітленням")
    print("2. Система безпеки")
    print("3. Розваги")
    print("4. Клімат-контроль")
    print("5. Голосові команди")
    print("6. Налаштування")
    print("7. Моніторинг енергії")
    print("0. Вихід")
    print("============================")


def lighting_menu(smart_home):
    """Меню керування освітленням"""
    while True:
        clear_console()
        print("\n=== КЕРУВАННЯ ОСВІТЛЕННЯМ ===")
        print("1. Увімкнути все світло")
        print("2. Вимкнути все світло")
        print("3. Налаштувати яскравість")
        print("4. Статус освітлення")
        print("0. Повернутися назад")

        choice = input("\nВаш вибір: ")

        if choice == "1":
            result = smart_home.control_lighting("ON")
            print(f"\n{result}")
        elif choice == "2":
            result = smart_home.control_lighting("OFF")
            print(f"\n{result}")
        elif choice == "3":
            try:
                level = int(input("Введіть рівень яскравості (0-100): "))
                result = smart_home.control_lighting("ADJUST", level)
                print(f"\n{result}")
            except ValueError:
                print("\nПомилка: Введіть число від 0 до 100")
        elif choice == "4":
            print(f"\nСтатус: {'Увімкнено' if smart_home.lighting.is_on else 'Вимкнено'}")
            print(f"Поточна яскравість: {smart_home.lighting.brightness}%")
        elif choice == "0":
            break

        input("\nНатисніть Enter для продовження...")


def security_menu(smart_home):
    """Меню системи безпеки"""
    while True:
        clear_console()
        print("\n=== СИСТЕМА БЕЗПЕКИ ===")
        print("1. Активувати охорону")
        print("2. Деактивувати охорону")
        print("3. Перевірити статус")
        print("4. Тестова тривога")
        print("0. Повернутися назад")

        choice = input("\nВаш вибір: ")

        if choice == "1":
            result = smart_home.activate_security_system()
            print(f"\n{result}")
        elif choice == "2":
            result = smart_home.deactivate_security_system()
            print(f"\n{result}")
        elif choice == "3":
            status = "Активна" if smart_home.security.armed else "Неактивна"
            alarm = "Тривога!" if smart_home.security.alarm_active else "Немає тривоги"
            print(f"\nСтатус охорони: {status}")
            print(f"Статус тривоги: {alarm}")
        elif choice == "4":
            result = smart_home.security.trigger_alarm()
            print(f"\n{result}")
        elif choice == "0":
            break

        input("\nНатисніть Enter для продовження...")


def entertainment_menu(smart_home):
    """Меню розваг"""
    while True:
        clear_console()
        print("\n=== СИСТЕМА РОЗВАГ ===")
        print("1. Увімкнути TV")
        print("2. Вимкнути TV")
        print("0. Повернутися назад")

        choice = input("\nВаш вибір: ")

        if choice == "1":
            result = smart_home.control_entertainment("TV", "ON")
            print(f"\n{result}")
        elif choice == "2":
            result = smart_home.control_entertainment("TV", "OFF")
            print(f"\n{result}")
        elif choice == "0":
            break

        input("\nНатисніть Enter для продовження...")


def climate_menu(smart_home):
    """Меню клімат-контролю"""
    while True:
        clear_console()
        print("\n=== КЛІМАТ-КОНТРОЛЬ ===")
        print("1. Увімкнути кондиціонер")
        print("2. Вимкнути кондиціонер")
        print("3. Встановити температуру")
        print("0. Повернутися назад")

        choice = input("\nВаш вибір: ")

        if choice == "1":
            result = smart_home.control_climate("ON")
            print(f"\n{result}")
        elif choice == "2":
            result = smart_home.control_climate("OFF")
            print(f"\n{result}")
        elif choice == "3":
            try:
                temp = int(input("Введіть бажану температуру (16-30°C): "))
                smart_home.settings.update_setting('default_temperature', temp)
                print(f"\nТемпературу встановлено на {temp}°C")
            except ValueError:
                print("\nПомилка: Введіть коректне значення температури")
        elif choice == "0":
            break

        input("\nНатисніть Enter для продовження...")


def voice_control_menu(smart_home, voice_control):
    """Меню голосового керування"""
    while True:
        clear_console()
        print("\n=== ГОЛОСОВЕ КЕРУВАННЯ ===")
        print("Доступні команди:")
        print("- turn on lights")
        print("- turn off lights")
        print("- activate security")
        print("- deactivate security")
        print("0. Повернутися назад")

        command = input("\nВведіть команду (0 для виходу): ")

        if command == "0":
            break

        result = voice_control.process_command(command)
        print(f"\n{result}")
        input("\nНатисніть Enter для продовження...")


def settings_menu(smart_home):
    """Меню налаштувань"""
    while True:
        clear_console()
        print("\n=== НАЛАШТУВАННЯ ===")
        print("1. Переглянути поточні налаштування")
        print("2. Змінити температуру за замовчуванням")
        print("3. Змінити яскравість за замовчуванням")
        print("0. Повернутися назад")

        choice = input("\nВаш вибір: ")

        if choice == "1":
            settings = smart_home.settings.settings
            print("\nПоточні налаштування:")
            for key, value in settings.items():
                print(f"{key}: {value}")
        elif choice == "2":
            try:
                temp = int(input("Введіть температуру за замовчуванням (16-30°C): "))
                smart_home.settings.update_setting('default_temperature', temp)
                print(f"\nТемпературу за замовчуванням встановлено на {temp}°C")
            except ValueError:
                print("\nПомилка: Введіть коректне значення температури")
        elif choice == "3":
            try:
                brightness = int(input("Введіть яскравість за замовчуванням (0-100%): "))
                smart_home.settings.update_setting('default_brightness', brightness)
                print(f"\nЯскравість за замовчуванням встановлено на {brightness}%")
            except ValueError:
                print("\nПомилка: Введіть коректне значення яскравості")
        elif choice == "0":
            break

        input("\nНатисніть Enter для продовження...")


def energy_menu(smart_home):
    """Меню моніторингу енергії"""
    while True:
        clear_console()
        print("\n=== МОНІТОРИНГ ЕНЕРГІЇ ===")
        print("1. Поточне споживання")
        print("2. Оптимізувати енергоспоживання")
        print("0. Повернутися назад")

        choice = input("\nВаш вибір: ")

        if choice == "1":
            usage = smart_home.energy.monitor_usage()
            print(f"\n{usage}")
        elif choice == "2":
            smart_home.energy.optimize_energy()
            print("\nЕнергоспоживання оптимізовано")
        elif choice == "0":
            break

        input("\nНатисніть Enter для продовження...")


def main():
    """Головна функція програми"""
    smart_home = SmartHomeFacade()
    voice_control = VoiceControl(smart_home)

    while True:
        clear_console()
        display_menu()
        choice = input("\nВаш вибір: ")

        if choice == "1":
            lighting_menu(smart_home)
        elif choice == "2":
            security_menu(smart_home)
        elif choice == "3":
            entertainment_menu(smart_home)
        elif choice == "4":
            climate_menu(smart_home)
        elif choice == "5":
            voice_control_menu(smart_home, voice_control)
        elif choice == "6":
            settings_menu(smart_home)
        elif choice == "7":
            energy_menu(smart_home)
        elif choice == "0":
            print("\nДякуємо за використання системи розумного дому!")
            break
        else:
            print("\nНеправильний вибір. Спробуйте ще раз.")
            time.sleep(1)


if __name__ == "__main__":
    main()