import json

account_balance = 100000
warehouse_products = [
    {
        "Produkt": "Płyta gipsowa",
        "Ilość": 1500,
        "Cena jednostkowa": 29.0
    }
]
operation_list = []
program_end = False

def save_data():
    with open("account_balance.txt", "w") as f:
        f.write(str(account_balance))

    with open("warhouse_products.txt", "w") as f:
        json.dump(warehouse_products, f)

    with open("operation_history.txt", "w") as f:
        for operation in operation_list:
            f.write(operation + '\n')

def load_data():
    global account_balance, warehouse_products, operation_list

    try:
        with open("account_balance.txt", "r") as f:
            account_balance = float(f.read())
    except FileNotFoundError:
        pass

    try:
        with open("warehouse_products.txt", "r") as f:
            warehouse_products = json.load(f)
    except FileNotFoundError:
        pass

    try:
        with open("operation_history.txt", "r") as f:
            operation_list = f.readlines()
    except FileNotFoundError:
        pass

print("Witaj w programie do zarządzania kontem firmy i magazynem!")

load_data()

while not program_end:
    operation = input("\nDostępne komendy:\n 1. Saldo\n 2. Sprzedaż\n 3. Zakup\n 4. Konto\n 5. Lista\n 6. Magazyn\n 7. Przegląd\n 8. Koniec\n")

    if operation == "1":
        amount = float(input("Podaj kwotę do dodania lub odjęcia z konta: "))
        account_balance += amount
        if amount > 0:
            print(f"\nKwota która została dodana to: {amount}")
            operation_list.append(f"Dodano: {amount} do konta firmy!")
        if amount < 0:
            print(f"\nKwota która została odjęta to: {amount}")
            operation_list.append(f"Odjęto: {amount} z konta firmy!")
        elif amount == 0: 
            print(f"\nNie dodano/odjęto żadnej kwoty!")

    elif operation == "2":
        sell_product = input("Podaj nazwę produktu: ")
        for product in warehouse_products:
            if product["Produkt"] == sell_product:
                unit_price_sell = float(input("Podaj cenę jednostkową: "))
                if unit_price_sell < 0:
                    print("Nieprawidłowa cena sprzedaży!")
                    break
                amount_of_products_sell = int(input("Podaj ilość: "))
                if product["Ilość"] >= amount_of_products_sell:
                    product["Ilość"] -= amount_of_products_sell
                    account_balance = account_balance + (unit_price_sell * amount_of_products_sell)
                    print("\nProdukt został sprzedany!")
                    operation_list.append(f"Sprzedano produkt o nazwie: {sell_product}, Cena jednostkowa: {unit_price_sell}, Ilość: {amount_of_products_sell}")
                    break
                else:
                    print("\nBrak wystarczającej ilości produktu w magazynie!")
                    operation_list.append(f"Próba sprzedania produktu o nazwie: {sell_product}, którego nie ma w wystarczającej ilości w magazynie!")
                    break
        else:
            print("\nBrak produktu w magazynie!")
            operation_list.append(f"Próba sprzedania produktu o nazwie: {sell_product}, którego nie ma w magazynie!")
                        
    elif operation == "3":
        purchase_product = input("Podaj nazwę produktu: ")
        amount_of_products = int(input("Podaj ilość: "))
        unit_price = float(input("Podaj cenę jednostkową: "))
        if account_balance >= amount_of_products * unit_price:
            warehouse_products.append({
                "Produkt": purchase_product,
                "Ilość": amount_of_products,
                "Cena jednostkowa": unit_price
            })
            account_balance = account_balance - (amount_of_products * unit_price)
            print(f"\nProdukt został dodany do magazynu!")
            operation_list.append(f"Zakupiono produkt o nazwie: {purchase_product}, Cena jednostkowa: {unit_price}, Ilość: {amount_of_products}")
            
        else:
            print("\nBrak wystarczających środków na koncie!")
            operation_list.append(f"Odrzucono zakup produktu o nazwie: {purchase_product} z powodu braku wystarczających środków na koncie!")
    
    elif operation == "4":
        print(f"\nAktualny stan konta: {account_balance}")
        operation_list.append("Sprawdzono aktualny stan konta!")

    elif operation == "5":
        print("\nStan magazynu:")
        for product in warehouse_products:
            print(f"{product['Produkt']}: {product['Ilość']} sztuk, Cena jednostkowa: {product['Cena jednostkowa']}")
            operation_list.append("Sprawdzono aktualny stan magazynu!")

    elif operation == "6":
        product_name = input("Podaj nazwę produktu: ")
        for product in warehouse_products:
            if product["Produkt"] == product_name:
                print(f"\nStan magazynu dla produktu '{product_name}': {product['Ilość']} sztuk, Cena jednostkowa: {product['Cena jednostkowa']}")
                operation_list.append(f"Sprawdzono aktualny stan magazynu dla produktu o nazwie: {product_name}")
                break
        else:
            print("\nBrak produktu w magazynie!")
            operation_list.append(f"Sprawdzono aktualny stan magazynu dla produktu o nazwie: {product_name}, którego nie ma w magazynie!")
    
    elif operation == "7":
        start_index = input("Podaj indeks początkowy: ")
        end_index = input("Podaj indeks końcowy: ")
        if start_index == "":
            start_index = 0
        else:
            start_index = int(start_index)
        if end_index == "":
            end_index = len(operation_list)
        else:
            end_index = int(end_index)
        if start_index < 0 or end_index < 0 or start_index > len(operation_list) or end_index > len(operation_list) or start_index > end_index:
            print("\nBłąd: Nieprawidłowy zakres!")
            print(f"Liczba zapisanych operacji: {len(operation_list)}")
            continue
        print("\nHistoria operacji:")
        print(operation_list[start_index:end_index])
    
    elif operation == "8":
        program_end = True

save_data()