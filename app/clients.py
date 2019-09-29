import csv
from datetime import date

from faker import Faker


class ValidThruClient:
    def __init__(self):
        self._cards = []
        self._clients = {}
        self._client_id_counter = 1

    def populate_from_csv(self, filepath):
        with open(filepath, newline="") as file:
            reader = csv.reader(file, delimiter="|")
            for line in reader:
                card = {
                    "client_id": int(line[0]),
                    "number": line[1],
                    "expiration_date": date(*[int(ymd) for ymd in line[2].split("-")]),
                }
                client = {
                    "name": line[3],
                    "address": line[4],
                    "dob": date(*[int(ymd) for ymd in line[5].split("-")]),
                }
                self._cards.append(card)
                try:
                    self._clients[int(line[0])]
                except KeyError:
                    self._clients[int(line[0])] = client
                    self._client_id_counter = int(line[0]) + 1

    def populate(self, amount):
        fake = Faker()
        for i in range(amount):
            client = {
                "name": fake.name(),
                "dob": fake.date_of_birth(),
                "address": fake.address().split("\n")[0],
            }
            month, year = fake.credit_card_expire().split("/")
            card = {
                "client_id": self._client_id_counter,
                "number": fake.credit_card_number(card_type="mastercard"),
                "expiration_date": date(int(f"20{year}"), int(f"{month}"), 1),
            }
            self._clients[self._client_id_counter] = client
            self._cards.append(card)
            self._client_id_counter += 1

    def cards_valid_thru_this_month_year(self, data):
        today = date.today()
        is_active = True
        if (data["year"] < today.year) or (
            data["year"] == today.year and data["month"] < today.month
        ):
            is_active = False

        near_to_expire = []
        for card in self._cards:
            if card["expiration_date"].year == data["year"]:
                if card["expiration_date"].month == data["month"]:
                    client = self._clients[card["client_id"]]
                    near_to_expire.append(
                        {
                            "client_id": card["client_id"],
                            "card_holder": client["name"],
                            "card_number": card["number"],
                            "month": data["month"],
                            "year": data["year"],
                            "is_active": is_active,
                        }
                    )
        return near_to_expire
