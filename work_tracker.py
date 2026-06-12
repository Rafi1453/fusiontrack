# FusionTrack - Work Inventory, Hours & Salary Tracker
# Author: Md Rafi Alam

import json
import os
import calendar
from datetime import datetime

INVENTORY_FILE = "inventory.json"
HOURS_FILE = "hours.json"
SALARY_FILE = "salary.json"

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def show_stock(inventory):
    if len(inventory) == 0:
        print("Stock is empty.")
    for i, p in enumerate(inventory, 1):
        print(i, "|", p.get("date", "-"), "|", p["name"], "|", p.get("supplier", "-"),
              "|", p.get("pallets", 0), "pallets |", p["total_pcs"], "pcs |", p["cost"], "EUR")

def ask_month():
    m_input = input("Month (mm.yyyy, Enter = this month): ")
    if m_input == "":
        now = datetime.now()
        return now.month, now.year
    month = int(m_input.split(".")[0])
    year = int(m_input.split(".")[1])
    return month, year

def month_hours(month, year):
    total = 0
    for s in hours_log:
        d, m, y = s["date"].split(".")
        if int(m) == month and int(y) == year:
            total = total + s["hours"]
    return round(total, 2)

inventory = load_data(INVENTORY_FILE)
hours_log = load_data(HOURS_FILE)
salaries = load_data(SALARY_FILE)
print("FusionTrack loaded -", len(inventory), "products,", len(hours_log), "shifts,", len(salaries), "salary records")

while True:
    print()
    print("===== FUSIONTRACK =====")
    print("1. Receive Product")
    print("2. View Stock")
    print("3. Edit Product")
    print("4. Delete Product")
    print("5. Log Work Shift")
    print("6. Monthly Work Calendar")
    print("7. Monthly Receive Report")
    print("8. Log Salary")
    print("9. Salary & Hours Report")
    print("10. Exit")

    choice = input("Choice (1-10): ")

    if choice == "1":
        date_str = input("Receive date (dd.mm.yyyy, Enter = today): ")
        if date_str == "":
            date_str = datetime.now().strftime("%d.%m.%Y")
        name = input("Product name: ")
        supplier = input("Company / supplier: ")
        pallets = int(input("How many pallets: "))
        cartons = int(input("How many cartons: "))
        boxes_per_carton = int(input("Boxes per carton: "))
        pcs_per_box = int(input("Pcs per box: "))
        cost = float(input("Total cost (EUR): "))
        total_pcs = cartons * boxes_per_carton * pcs_per_box
        product = {
            "date": date_str, "name": name, "supplier": supplier,
            "pallets": pallets, "cartons": cartons,
            "boxes_per_carton": boxes_per_carton, "pcs_per_box": pcs_per_box,
            "total_pcs": total_pcs, "cost": cost
        }
        inventory.append(product)
        save_data(INVENTORY_FILE, inventory)
        print("Received:", name, "from", supplier, "-", total_pcs, "pcs,", pallets, "pallets")

    elif choice == "2":
        show_stock(inventory)

    elif choice == "3":
        show_stock(inventory)
        num = int(input("Which number to edit? "))
        p = inventory[num - 1]
        print("Editing:", p["name"], "(press Enter to keep old value)")
        new_date = input("Date [" + p.get("date", "-") + "]: ")
        if new_date != "":
            p["date"] = new_date
        new_name = input("Name [" + p["name"] + "]: ")
        if new_name != "":
            p["name"] = new_name
        new_supplier = input("Supplier [" + p.get("supplier", "-") + "]: ")
        if new_supplier != "":
            p["supplier"] = new_supplier
        new_pallets = input("Pallets [" + str(p.get("pallets", 0)) + "]: ")
        if new_pallets != "":
            p["pallets"] = int(new_pallets)
        new_cartons = input("Cartons [" + str(p["cartons"]) + "]: ")
        if new_cartons != "":
            p["cartons"] = int(new_cartons)
        new_bpc = input("Boxes per carton [" + str(p["boxes_per_carton"]) + "]: ")
        if new_bpc != "":
            p["boxes_per_carton"] = int(new_bpc)
        new_ppb = input("Pcs per box [" + str(p["pcs_per_box"]) + "]: ")
        if new_ppb != "":
            p["pcs_per_box"] = int(new_ppb)
        new_cost = input("Cost [" + str(p["cost"]) + "]: ")
        if new_cost != "":
            p["cost"] = float(new_cost)
        p["total_pcs"] = p["cartons"] * p["boxes_per_carton"] * p["pcs_per_box"]
        save_data(INVENTORY_FILE, inventory)
        print("Updated:", p["name"], "-", p["total_pcs"], "pcs")

    elif choice == "4":
        show_stock(inventory)
        num = int(input("Which number to delete? "))
        removed = inventory.pop(num - 1)
        save_data(INVENTORY_FILE, inventory)
        print("Deleted:", removed["name"])

    elif choice == "5":
        date_str = input("Date (dd.mm.yyyy, Enter = today): ")
        if date_str == "":
            date_str = datetime.now().strftime("%d.%m.%Y")
        start = input("Start time (HH:MM): ")
        end = input("End time (HH:MM): ")
        t1 = datetime.strptime(start, "%H:%M")
        t2 = datetime.strptime(end, "%H:%M")
        worked = (t2 - t1).total_seconds() / 3600
        if worked < 0:
            worked = worked + 24
        worked = round(worked, 2)
        shift = {"date": date_str, "start": start, "end": end, "hours": worked}
        hours_log.append(shift)
        save_data(HOURS_FILE, hours_log)
        print("Logged:", date_str, start, "-", end, "=", worked, "hours")

    elif choice == "6":
        month, year = ask_month()
        day_hours = {}
        for s in hours_log:
            d, m, y = s["date"].split(".")
            if int(m) == month and int(y) == year:
                day = int(d)
                day_hours[day] = day_hours.get(day, 0) + s["hours"]
        print()
        print("      ", calendar.month_name[month], year)
        print("Mon  Tue  Wed  Thu  Fri  Sat  Sun")
        for week in calendar.monthcalendar(year, month):
            row = ""
            for day in week:
                if day == 0:
                    row = row + "     "
                elif day in day_hours:
                    row = row + str(day).rjust(2) + "*  "
                else:
                    row = row + str(day).rjust(2) + "   "
            print(row)
        print()
        print("--- Work days (* marked) ---")
        for s in hours_log:
            d, m, y = s["date"].split(".")
            if int(m) == month and int(y) == year:
                print(s["date"], "|", s["start"], "-", s["end"], "|", s["hours"], "h")
        print("TOTAL:", month_hours(month, year), "hours")

    elif choice == "7":
        month, year = ask_month()
        print()
        print("--- RECEIVE REPORT:", calendar.month_name[month], year, "---")
        total_cost = 0
        total_pallets = 0
        count = 0
        for p in inventory:
            if "date" not in p:
                continue
            d, m, y = p["date"].split(".")
            if int(m) == month and int(y) == year:
                print(p["date"], "|", p["name"], "|", p.get("supplier", "-"),
                      "|", p.get("pallets", 0), "pallets |", p["total_pcs"], "pcs |", p["cost"], "EUR")
                total_cost = total_cost + p["cost"]
                total_pallets = total_pallets + p.get("pallets", 0)
                count = count + 1
        print("-------------------------------")
        print("Deliveries:", count)
        print("Total pallets:", total_pallets)
        print("TOTAL COST:", round(total_cost, 2), "EUR")

    elif choice == "8":
        month_str = input("Salary month (mm.yyyy): ")
        amount = float(input("Salary amount (EUR): "))
        note = input("Note (optional): ")
        salaries.append({"month": month_str, "amount": amount, "note": note})
        save_data(SALARY_FILE, salaries)
        print("Salary logged:", month_str, "-", amount, "EUR")

    elif choice == "9":
        print()
        print("--- SALARY & HOURS REPORT ---")
        total_salary = 0
        for s in salaries:
            month = int(s["month"].split(".")[0])
            year = int(s["month"].split(".")[1])
            hrs = month_hours(month, year)
            print(s["month"], "|", hrs, "hours |", s["amount"], "EUR |", s["note"])
            total_salary = total_salary + s["amount"]
        print("-------------------------------")
        print("TOTAL EARNED:", round(total_salary, 2), "EUR")

    elif choice == "10":
        print("Goodbye!")
        break

    else:
        print("Please enter 1-10.")