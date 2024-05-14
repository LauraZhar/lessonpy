
from smartphone import Smartphone

 
catalog = [
    Smartphone("Apple", "iPhone 12", "+79111234567"),
    Smartphone("Samsung", "Galaxy S21", "+79217654321"),
    Smartphone("Google", "Pixel 5", "+79301112233"),
    Smartphone("OnePlus", "9 Pro", "+79445556677"),
    Smartphone("Xiaomi", "Mi 11", "+79553334455")
]

 
for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.phone_number}")
