"""
Attendance Tracker using Lists and Dictionaries

Data structure:
  attendance = { "Student Name": ["P", "A", "P", ...] }
  - DICT: maps each student to their record (fast lookup by name)
  - LIST: one entry per class day, in order ("P" = present, "A" = absent)
"""

VALID = ("P", "A")


def add_student(attendance, name):
    name = name.strip()
    if not name:
        return False, "Name cannot be empty."
    if name in attendance:
        return False, f"'{name}' already exists."
    attendance[name] = []
    return True, f"Added '{name}'."


def mark_day(attendance, statuses):
    """Record one new class day. statuses = {name: 'P'/'A'}; unlisted students count as absent."""
    for name, s in statuses.items():
        if name not in attendance:
            return False, f"'{name}' not found."
        if s.upper() not in VALID:
            return False, f"Invalid status '{s}' for {name} (use P or A)."
    for name in attendance:
        attendance[name].append(statuses.get(name, "A").upper())
    return True, "Attendance recorded."


def update_attendance(attendance, name, day, status):
    """Correct an earlier entry. day is 1-based."""
    if name not in attendance:
        return False, f"'{name}' not found."
    if status.upper() not in VALID:
        return False, "Status must be P or A."
    if not 1 <= day <= len(attendance[name]):
        return False, f"Day {day} has no record for {name}."
    attendance[name][day - 1] = status.upper()
    return True, f"Updated {name}, day {day} -> {status.upper()}."


def percentage(records):
    return 0.0 if not records else records.count("P") / len(records) * 100


def below_threshold(attendance, threshold=75):
    return {n: round(percentage(r), 1) for n, r in attendance.items()
            if r and percentage(r) < threshold}


def display(attendance, threshold=75):
    if not attendance:
        print("  (no students)")
        return
    days = max(len(r) for r in attendance.values())
    header = f"{'Student':<12}" + "".join(f"D{d:<3}" for d in range(1, days + 1))
    print(header + f"{'Present':>9}{'  %':>8}  Status")
    print("-" * (len(header) + 28))
    for name, rec in attendance.items():
        pct = percentage(rec)
        row = f"{name:<12}" + "".join(f"{s:<4}" for s in rec) + "    " * (days - len(rec))
        flag = "SHORTAGE" if rec and pct < threshold else "OK"
        print(f"{row}{rec.count('P'):>6}/{len(rec):<2}{pct:>7.1f}%  {flag}")


def run_tests():
    a = {}
    for n in ("Asha", "Ravi", "Meena"):
        assert add_student(a, n)[0]
    assert not add_student(a, "Asha")[0]            # duplicate
    assert not add_student(a, "  ")[0]              # empty

    # Scenario 1: normal week
    mark_day(a, {"Asha": "P", "Ravi": "P", "Meena": "A"})
    mark_day(a, {"Asha": "P", "Ravi": "A", "Meena": "A"})
    mark_day(a, {"Asha": "P", "Ravi": "P", "Meena": "A"})
    mark_day(a, {"Asha": "P", "Ravi": "P"})          # Meena missing -> absent
    assert percentage(a["Asha"]) == 100
    assert percentage(a["Ravi"]) == 75
    assert percentage(a["Meena"]) == 0
    assert below_threshold(a, 75) == {"Meena": 0.0}  # Ravi is exactly 75 -> not below
    assert set(below_threshold(a, 80)) == {"Ravi", "Meena"}

    # Scenario 2: update
    assert update_attendance(a, "Ravi", 2, "p")[0]
    assert percentage(a["Ravi"]) == 100
    assert not update_attendance(a, "Ravi", 9, "P")[0]
    assert not update_attendance(a, "Ravi", 1, "X")[0]
    assert not update_attendance(a, "Zed", 1, "P")[0]

    # Scenario 3: invalid input leaves data unchanged
    before = {k: v[:] for k, v in a.items()}
    assert not mark_day(a, {"Asha": "Q"})[0]
    assert not mark_day(a, {"Ghost": "P"})[0]
    assert a == before

    # Scenario 4: student with no records, student added late
    add_student(a, "Late")
    assert percentage(a["Late"]) == 0 and "Late" not in below_threshold(a)
    print("All attendance tests passed.")


def main():
    run_tests()
    attendance = {}
    for n in ("Asha", "Ravi", "Meena", "Kabir"):
        add_student(attendance, n)
    week = [
        {"Asha": "P", "Ravi": "P", "Meena": "P", "Kabir": "A"},
        {"Asha": "P", "Ravi": "A", "Meena": "P", "Kabir": "A"},
        {"Asha": "P", "Ravi": "P", "Meena": "A", "Kabir": "A"},
        {"Asha": "A", "Ravi": "P", "Meena": "P", "Kabir": "P"},
    ]
    for day in week:
        mark_day(attendance, day)

    print("\n=== SAMPLE CLASS ===")
    display(attendance)
    low = below_threshold(attendance, 75)
    print("\nBelow 75%:", ", ".join(f"{n} ({p}%)" for n, p in low.items()) or "none")

    menu = ("\n1. Add student  2. Mark today's attendance  3. Update a record  "
            "4. Display  5. Shortage list  6. Exit")
    while True:
        print(menu)
        c = input("Choice: ").strip()
        if c == "1":
            print(add_student(attendance, input("Name: "))[1])
        elif c == "2":
            st = {n: input(f"  {n} (P/A): ").strip() or "A" for n in attendance}
            print(mark_day(attendance, st)[1])
        elif c == "3":
            try:
                print(update_attendance(attendance, input("Name: ").strip(),
                                        int(input("Day number: ")), input("New status (P/A): "))[1])
            except ValueError:
                print("Day must be a number.")
        elif c == "4":
            display(attendance)
        elif c == "5":
            try:
                t = float(input("Threshold %: "))
                print(below_threshold(attendance, t) or "No one is below the threshold.")
            except ValueError:
                print("Enter a number.")
        elif c == "6":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
OUTPUT:


"""
Sales Data Analyzer using Lists and Dictionaries

Data structure:
  products = [ {"name": "Pen", "price": 10.0, "quantity": 120}, ... ]
  - LIST : holds all products (easy to loop, sort and rank)
  - DICT : one product's fields (name, price, quantity sold)
"""


def find_product(products, name):
    for p in products:
        if p["name"].lower() == name.strip().lower():
            return p
    return None


def add_product(products, name, price, quantity):
    """Add a new product with its price and units sold so far."""
    if not name.strip():
        return False, "Name cannot be empty."
    if price < 0 or quantity < 0:
        return False, "Price and quantity cannot be negative."
    if find_product(products, name):
        return False, f"'{name}' already exists (use record_sale or update_product)."
    products.append({"name": name.strip(), "price": float(price), "quantity": int(quantity)})
    return True, f"Added '{name.strip()}'."


def record_sale(products, name, units):
    """Add newly sold units to an existing product."""
    p = find_product(products, name)
    if p is None:
        return False, f"'{name}' not found."
    if units <= 0:
        return False, "Units must be positive."
    p["quantity"] += int(units)
    return True, f"{units} unit(s) of {p['name']} sold."


def update_product(products, name, price=None, quantity=None):
    """Overwrite price and/or quantity (e.g. to correct a mistake)."""
    p = find_product(products, name)
    if p is None:
        return False, f"'{name}' not found."
    if (price is not None and price < 0) or (quantity is not None and quantity < 0):
        return False, "Values cannot be negative."
    if price is not None:
        p["price"] = float(price)
    if quantity is not None:
        p["quantity"] = int(quantity)
    return True, f"Updated '{p['name']}'."


def revenue_by_product(products):
    """Return {name: price * quantity}."""
    return {p["name"]: p["price"] * p["quantity"] for p in products}


def total_sales(products):
    return sum(revenue_by_product(products).values())


def top_by_quantity(products):
    """Highest-selling product by units. Returns a list (so ties are visible)."""
    if not products:
        return []
    best = max(p["quantity"] for p in products)
    return [p["name"] for p in products if p["quantity"] == best]


def top_by_revenue(products):
    rev = revenue_by_product(products)
    if not rev:
        return []
    best = max(rev.values())
    return [n for n, r in rev.items() if r == best]


def summary(products):
    total = total_sales(products)
    print(f"\n{'Product':<12}{'Price':>9}{'Units':>8}{'Revenue':>12}{'Share':>8}")
    print("-" * 49)
    for p in sorted(products, key=lambda p: p["price"] * p["quantity"], reverse=True):
        rev = p["price"] * p["quantity"]
        share = rev / total * 100 if total else 0
        print(f"{p['name']:<12}{p['price']:>9.2f}{p['quantity']:>8}{rev:>12.2f}{share:>7.1f}%")
    print("-" * 49)
    print(f"{'TOTAL':<29}{total:>20.2f}")
    if products:
        print(f"\nMost units sold : {', '.join(top_by_quantity(products))}")
        print(f"Highest revenue : {', '.join(top_by_revenue(products))}")
        avg = total / len(products)
        under = [p["name"] for p in products if p["price"] * p["quantity"] < avg]
        print(f"Average revenue per product: {avg:.2f}")
        print(f"Below average   : {', '.join(under) or 'none'}")


def run_tests():
    # Dataset 1: ordinary
    d1 = []
    add_product(d1, "Pen", 10, 100)         # 1000
    add_product(d1, "Notebook", 50, 40)     # 2000
    add_product(d1, "Bag", 500, 5)          # 2500
    assert total_sales(d1) == 5500
    assert revenue_by_product(d1) == {"Pen": 1000, "Notebook": 2000, "Bag": 2500}
    assert top_by_quantity(d1) == ["Pen"]    # most units but lowest revenue
    assert top_by_revenue(d1) == ["Bag"]     # fewest units but highest revenue

    # add / update / record
    assert not add_product(d1, "pen", 5, 5)[0]          # duplicate
    assert not add_product(d1, "X", -1, 5)[0]
    assert record_sale(d1, "Bag", 3)[0] and find_product(d1, "Bag")["quantity"] == 8
    assert not record_sale(d1, "Bag", 0)[0]
    assert not record_sale(d1, "Ghost", 1)[0]
    assert update_product(d1, "Pen", price=12)[0] and total_sales(d1) == 1200 + 2000 + 4000
    assert not update_product(d1, "Pen", quantity=-5)[0]

    # Dataset 2: tie in units
    d2 = []
    add_product(d2, "A", 5, 10)
    add_product(d2, "B", 8, 10)
    assert top_by_quantity(d2) == ["A", "B"]
    assert top_by_revenue(d2) == ["B"]

    # Dataset 3: empty and zero sales
    assert total_sales([]) == 0 and top_by_quantity([]) == [] and top_by_revenue([]) == []
    d3 = []
    add_product(d3, "Unsold", 99, 0)
    assert total_sales(d3) == 0
    print("All sales analyzer tests passed.")


def main():
    run_tests()
    products = []
    for name, price, qty in [("Pen", 10, 120), ("Notebook", 45, 60), ("Bag", 650, 8),
                             ("Geometry Box", 120, 25), ("Marker", 30, 45)]:
        add_product(products, name, price, qty)
    print("\n=== SAMPLE STATIONERY SHOP ===")
    summary(products)

    menu = "\n1. Add product  2. Record sale  3. Update product  4. Summary  5. Exit"
    while True:
        print(menu)
        c = input("Choice: ").strip()
        try:
            if c == "1":
                print(add_product(products, input("Name: "), float(input("Price: ")),
                                  int(input("Units sold: ")))[1])
            elif c == "2":
                print(record_sale(products, input("Name: "), int(input("Units sold: ")))[1])
            elif c == "3":
                name = input("Name: ")
                p, q = input("New price (blank = keep): "), input("New quantity (blank = keep): ")
                print(update_product(products, name, float(p) if p else None,
                                     int(q) if q else None)[1])
            elif c == "4":
                summary(products)
            elif c == "5":
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter valid numbers.")


if __name__ == "__main__":
    main()



