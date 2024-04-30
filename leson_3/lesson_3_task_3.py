
from mailing import Mailing
from address import Address

 
to_address = Address("123456", "Астана", "Достык", "13", "50")
from_address = Address("654321", "Алматы", "пр. Абая", "25", "12")

 
mail = Mailing(to_address, from_address, 350, "kz1234567890")

# Вывод информации о почтовом отправлении
print(f"Отправление {mail.track} из {mail.from_address.index}, {mail.from_address.city}, {mail.from_address.street}, {mail.from_address.house} - {mail.from_address.apartment} в {mail.to_address.index}, {mail.to_address.city}, {mail.to_address.street}, {mail.to_address.house} - {mail.to_address.apartment}. Стоимость {mail.cost} рублей.")
