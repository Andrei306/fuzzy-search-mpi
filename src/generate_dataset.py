import random


FIRST_NAMES = [
    "Andrei", "Andreea", "Andra", "Adrian", "Adriana", "Ion", "Ionut", "Ioana", "Ioan",
    "Maria", "Marian", "Marius", "Mariana", "Alex", "Alexandru", "Alexandra",
    "Elena", "George", "Georgiana", "Mihai", "Mihaela", "Cristian", "Cristina",
    "Radu", "Raluca", "Robert", "Roberta", "Daniel", "Daniela", "Gabriel", "Gabriela",
    "Stefan", "Stefan", "Ana", "Anca", "Bianca", "Carmen", "David", "Eduard", "Florin", "Larisa",
    "Lucian", "Matei", "Nicoleta", "Ovidiu", "Paula", "Paul", "Sebastian", "Sorin", 
    "Teodora", "Victor", "Vlad", "Vladimir", "Claudiu", "Corina", "Denisa", "Darius",
    "Emanuel", "Felicia", "Horatiu", "Irina", "Larisa", "Lavinia", "Nicolae", "Patricia",
    "Silviu", "Tudor", "Valentin"
]

LAST_NAMES = [
    "Popescu", "Popa", "Pop", "Ionescu", "Ion", "Georgescu", "Dumitrescu", "Stan", "Stoica",
    "Radu", "Marinescu", "Diaconu", "Tudor", "Munteanu", "Dobre", "Matei", "Nistor", "Petrescu", "Iliescu",
    "Enache", "Constantinescu", "Dragomir", "Luca", "Dinu", "Pavel", "Fratila", "Voicu", "Neagu", "Mocanu",
    "Preda", "Barbu", "Sandu", "Toma", "Vasile", "Serban", "Avram", "Balan", "Cojocaru", "Filip",
    "Grigore", "Lazar", "Manole", "Niculescu", "Oprea", "Rosu", "Stanciu", "Ursu", "Zamfir"
]

INTERNATIONAL_FIRST = [
    "John", "Michael", "Emily", "Sophia", "James",
    "Emma", "Olivia", "Liam", "Noah", "Lucas",
    "Charlotte", "Amelia", "Benjamin", "Ethan"
]

INTERNATIONAL_LAST = [
    "Smith", "Johnson", "Brown", "Williams",
    "Miller", "Davis", "Wilson", "Moore",
    "Taylor", "Anderson"
]


def introduce_typo(name):
    """
    Introduce random typo with small probability.
    """

    if len(name) < 4:
        return name

    operations = ["swap", "delete", "replace"]

    op = random.choice(operations)

    idx = random.randint(0, len(name) - 2)

    chars = "abcdefghijklmnopqrstuvwxyz"

    if op == "swap":
        lst = list(name)
        lst[idx], lst[idx + 1] = lst[idx + 1], lst[idx]
        return "".join(lst)

    elif op == "delete":
        return name[:idx] + name[idx + 1:]

    elif op == "replace":
        return (
            name[:idx]
            + random.choice(chars)
            + name[idx + 1:]
        )

    return name


def generate_name():
    """
    Generate a realistic random name.
    """

    if random.random() < 0.8:
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
    else:
        first = random.choice(INTERNATIONAL_FIRST)
        last = random.choice(INTERNATIONAL_LAST)

    full_name = f"{first} {last}"

    # Add middle name sometimes
    if random.random() < 0.15:
        middle = random.choice(FIRST_NAMES)
        full_name = f"{first} {middle} {last}"

    # Introduce typo sometimes
    if random.random() < 0.08:
        full_name = introduce_typo(full_name)

    return full_name


def main():
    output_file = "data/names.txt"

    count = 1_000_000

    with open(output_file, "w", encoding="utf-8") as f:
        for _ in range(count):
            f.write(generate_name() + "\n")

    print(f"Generated {count:,} names")


if __name__ == "__main__":
    main()