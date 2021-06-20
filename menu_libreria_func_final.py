# Gestiona una librería virtual
# Podrá buscar libros por los siguientes parámetros: (id, author, Titulo, Genero)
# Ademas, se podrá añadir nuevo libro, modificar los datos de cada uno de ellos y eliminarlos
# Crear opcion para exportar los datos a un excel
# La BBDD vendra en un archivo json

# IMPORTS NECESARIOS
import string
import random
import json
import csv

# FUNCIONES
def menu_principal():   # IMPRIMIR MENU PRINCIPAL
    print("Bookshop".center(50, '-'))
    print("MENU PRINCIPAL".center(50,'-'))
    for i in range (1, len(menu_options)):  
        print(f"{i}. {menu_options[i].capitalize()}")
    print("Q. EXIT")

def book_by_id(id_book, libreria):
    for book in libreria:
        if book["id"] == id_book:
            print("------------")
            return book #break DEVOLVERÁ EL LIBRO APENAS ENCUENTRE UNA COINCIDENCIA

def books_by_key(libreria, key):
    result = []
    print(f"Opcion {menu_options[int(key)].upper()}")
    if key=='2' or key=='3':    # Busqueda texto introducido por teclado
        search_term = input(f"{menu_options[int(key)]} to search: ").lower()
        for book in libreria:
            if book[menu_options[int(key)]].lower().find(search_term.lower()) >= 0:
                result.append(book)
    elif key=='4':  # Busqueda por opciones disponibles
        list_aux = print_options_genre()
        search_term = input(f"{menu_options[int(key)]} to search: ").lower()
        for i in list_aux:
            list_aux[i] = str(list_aux[i])  # Pasamos la lista de enteros a tipo str para comprobar la opcion marcada por el usuario
        if search_term in list_aux:
            for book in libreria:
                if book[menu_options[int(user_option)]] == genre[int(search_term)]:
                    result.append(book)
    return result

def print_pretty(book_to_print):
    if book_to_print != None:
        if isinstance(book_to_print, dict):
            for k, v in book_to_print.items():
                    print(f"{k}: {v}")
        elif isinstance(book_to_print, list):
            print(f"Libros encontrados: {len(book_to_print)}")
            print("------------")
            for i, book in enumerate(book_to_print):
                print(f"LIBRO {i+1}")
                for k, v in book.items():
                    print(f"{k}: {v}")
                input("Continue...")
                print("------------")
            print(f"Libros encontrados: {len(book_to_print)}")
    else:
        print("Resultado no encontrado")

def print_options_genre():
    list_genre = list(range(len(genre)))  # Creamos una lista con el numero max de opciones de genero por si en un futuro se añaden mas
    print("Opciones disponibles:")
    for i in range (len(genre)): # impresion de los generos disponibles
        print(f"{i}. {genre[i]}")
    print("------------")
    return list_genre

def id_generator(size=3, first_chars=string.ascii_lowercase, second_chars=string.ascii_lowercase + string.digits):
    id_control = False
    list_id = []
    for book in bookshop:
        list_id.append(book["id"])
    while id_control == False:
        id_new =  ''.join(random.choice(first_chars) for _ in range(size-1)) + "_" + ''.join(random.choice(second_chars) for _ in range(size))
        if id_new not in list_id:
            id_control = True
    return id_new

def create_book(bookshop, key):
    print(f"Opcion {menu_options[int(key)].upper()}")
    new_book = {}
    for k in keys_books:
        if k == "id":
            new_book[k] = id_generator()
            print(f"id asignado: {new_book[k]}")
        elif k != 'genre' and k != 'id':
            new_book[k] = input(f"{k}: ")
        elif k == "genre":
            print(f"{k.upper()} disponibles:")
            for i in range (len(genre)): # impresion de los generos disponibles
                print(i ,".", genre[i])
            new_book[k] = genre[int(input(f"{k.upper()}: "))]
    bookshop.append(new_book)
    print("------------")
    print("Libro Creado:")
    print_pretty(new_book)

def modify_book(bookshop, user_option):
    print(f"Opcion {menu_options[int(user_option)].upper()}")
    user_id = input(f"id search: ")
    book = book_by_id(user_id, bookshop)
    print_pretty(book)
    if book != None:
        print("------------")
        for i, key in enumerate(keys_books):
            if key != "id":
                print(f"{i}. {key}")
            else:
                pass
        user = int(input("Campo a modificar: "))
        print("------------")
        key = keys_books[user]
        print(f"Valor a modificar --> {book[key]}")
        bookshop.remove(book)
        if key != "genre" and key != "id":
            book[key] = input("Nuevo valor: ")
        elif key == "genre":
            print_options_genre()
            option_genre = int(input("Elija opcion: "))
            book[key] = genre[option_genre]
        bookshop.append(book)
        print("------------")
        print("Libro Modificado:")
        print_pretty(book)

def delete_book(bookshop, user_option):
    print(f"Opcion {menu_options[int(user_option)].upper()}")
    user = input("id: ")
    book = book_by_id(user, bookshop)
    print("------------")
    print_pretty(book)
    if book != None:
        user = input("Está seguro que desea eliminar el libro (y/n): ").lower()
        if user == "y":
            bookshop.remove(book)
            print("------------")
            print("Eliminando registro...")

def write_data():
    with open("./bookshop.json", "w", encoding="utf8") as file:
        json.dump({"books":bookshop}, file, ensure_ascii=False, indent=4)

def export_book_to_excel():
    with open("./bookshop.json", encoding="utf8") as file:
        bookshop = json.load(file)["books"]
    with open("./export_bookshop.csv", "w", newline="") as file:
        csv_writer = csv.writer(file, delimiter=",")
        csv_writer.writerow(bookshop[0].keys())
        #[csv_writer.writerow(book.values()) for book in bookshop]
        for book in bookshop:
            csv_writer.writerow(book.values())
    print("Archivo exportado a formato Excel con el nombre: 'export_bookshop.csv'")

# Leemos la BBDD
with open("./bookshop.json", encoding="utf8") as file:
    bookshop = json.load(file)["books"]

# VARIABLES
keys_books = list(bookshop[0].keys())   # ['id', 'title', 'author', 'genre']
options = ["New Book", "Modify book", "Delete book", "Exportar a Excel", "Total libros en BBDD"]
menu_options = ["exit"] + keys_books + options
genre = ["Narrativa extranjera", "Divulgación científica", "Narrativa policíaca", "Ciencia ficción", "Autoayuda", "Manga"]
exit_principal = True   # controla el flujo del menu principal

# Programa
while exit_principal == True:
    menu_principal()
    user_option = input("Introduzca opcion: ").upper()
    print("-----------------------")
    if user_option == 'Q':
        print("Cerrando el programa......")
        exit_principal = False  # Sale del programa
    elif user_option == '1':    #ID
        print(f"Opcion {menu_options[int(user_option)].upper()}")
        user_id = input(f"{menu_options[int(user_option)]} to search: ")
        book = book_by_id(user_id, bookshop)
        print_pretty(book)
    elif user_option == '2':    #TITLE
        books_search = books_by_key(bookshop, user_option)
        print_pretty(books_search)
    elif user_option == '3':    #AUTHOR
        books_search = books_by_key(bookshop, user_option)
        print_pretty(books_search)
    elif user_option == '4':    #GENER
        books_search = books_by_key(bookshop, user_option)
        print_pretty(books_search)
    elif user_option == '5':    # New Book
        create_book(bookshop, user_option)
        write_data()
    elif  user_option == '6':   # Modify Book
        modify_book(bookshop, user_option)
        write_data()
    elif  user_option == '7':   # Delete Book
        delete_book(bookshop, user_option)
        write_data()
    elif  user_option == '8':   # Exportar a Excell
        print(f"Opcion {menu_options[int(user_option)].upper()}")
        export_book_to_excel()
    elif  user_option == '9':   # Num total libros
        print(f"Opcion {menu_options[int(user_option)].upper()}")
        print(f"TOTAL de libros en la BBDD: {len(bookshop)}")
    else:
        print("OPCION INCORRECTA")