import os
import re
from database import con, cur 

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def es_email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def usuario_existe(ide_number, email):
    cur.execute('SELECT COUNT(*) FROM users WHERE ide_number = ? OR email = ?', (ide_number, email))
    return cur.fetchone()[0] > 0

def mostrar_tabla(datos, encabezados):
    print("\n" + "-" * 100)
    print(" | ".join(encabezados))
    print("-" * 100)
    for fila in datos:
        print(" | ".join(str(col) if col is not None else "" for col in fila))
    print("-" * 100 + "\n")

def crear_usuario():
    limpiar_pantalla()
    fname = input('Nombre: ')
    lname = input('Apellido: ')
    ide_num = input('Número de identificación: ')
    email = input('Correo electrónico: ')
    estado = input('Estado del usuario (1=Activo, 0=Inactivo): ')

    if not es_email_valido(email):
        print("⚠️ Correo inválido.")
        return

    if estado not in ['0', '1']:
        print("⚠️ Estado inválido. Debe ser 0 o 1.")
        return

    if usuario_existe(ide_num, email):
        print('❌ Ya existe un usuario con ese número de ID o correo.')
        return

    con.execute('''
        INSERT INTO users (firstname, lastname, ide_number, email, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (fname, lname, ide_num, email, int(estado)))
    con.commit()
    print('✅ Usuario creado exitosamente.')

def listar_usuarios(filtrar_estado=None):
    limpiar_pantalla()
    consulta = '''
        SELECT 
            id, firstname, lastname, email, ide_number,
            CASE WHEN status = 1 THEN 'Activo' ELSE 'Inactivo' END AS Estado,
            created_at, updated_at
        FROM users
        WHERE deleted_at IS NULL
    '''
    if filtrar_estado is not None:
        consulta += ' AND status = ?'
        cur.execute(consulta, (filtrar_estado,))
    else:
        cur.execute(consulta)

    datos = cur.fetchall()
    if datos:
        encabezados = ["ID", "Nombre", "Apellido", "Correo", "Identificación", "Estado", "Creado", "Actualizado"]
        mostrar_tabla(datos, encabezados)
    else:
        print("📭 No hay usuarios registrados.")

def actualizar_usuario():
    limpiar_pantalla()
    ide_num = input("ID del usuario a actualizar: ")
    cur.execute('SELECT * FROM users WHERE ide_number = ? AND deleted_at IS NULL', (ide_num,))
    usuario = cur.fetchone()

    if not usuario:
        print("❌ Usuario no encontrado.")
        return

    print(f"\n🔎 Usuario actual: {usuario[1]} {usuario[2]}, correo: {usuario[4]}, estado: {'Activo' if usuario[5] == 1 else 'Inactivo'}\n")

    nuevo_nombre = input("Nuevo nombre: ")
    nuevo_apellido = input("Nuevo apellido: ")
    nuevo_email = input("Nuevo correo: ")
    nuevo_estado = input("Nuevo estado (1=Activo, 0=Inactivo): ")

    if not es_email_valido(nuevo_email):
        print("⚠️ Correo inválido.")
        return

    if nuevo_estado not in ['0', '1']:
        print("⚠️ Estado inválido. Debe ser 0 o 1.")
        return

    con.execute('''
        UPDATE users
        SET firstname = ?, lastname = ?, email = ?, status = ?, updated_at = datetime('now','localtime')
        WHERE ide_number = ?
    ''', (nuevo_nombre, nuevo_apellido, nuevo_email, int(nuevo_estado), ide_num))
    con.commit()
    print("✅ Usuario actualizado.")

def eliminar_usuario_logico():
    limpiar_pantalla()
    ide_num = input("ID del usuario a eliminar: ")
    confirmar = input(f"¿Está seguro que desea eliminar al usuario con ID {ide_num}? (s/n): ").lower()
    if confirmar != 's':
        print("❎ Operación cancelada.")
        return

    con.execute('''
        UPDATE users
        SET status = 0, deleted_at = datetime('now','localtime')
        WHERE ide_number = ?
    ''', (ide_num,))
    con.commit()
    print("🗑️ Usuario eliminado correctamente.")

def buscar_usuario():
    limpiar_pantalla()
    palabra = input("Buscar por nombre o correo: ").lower()
    cur.execute('''
        SELECT 
            id, firstname, lastname, email, ide_number,
            CASE WHEN status = 1 THEN 'Activo' ELSE 'Inactivo' END AS Estado
        FROM users
        WHERE deleted_at IS NULL AND (LOWER(firstname) LIKE ? OR LOWER(email) LIKE ?)
    ''', (f'%{palabra}%', f'%{palabra}%'))
    resultados = cur.fetchall()
    if resultados:
        encabezados = ["ID", "Nombre", "Apellido", "Correo", "Identificación", "Estado"]
        mostrar_tabla(resultados, encabezados)
    else:
        print("🔍 No se encontraron coincidencias.")

def menu_principal():
    while True:
        print("\n::: 📋 Menú Principal 📋 :::")
        print("-> [1] Crear nuevo usuario <-")
        print("-> [2] Listar todos los usuarios <-")
        print("-> [3] Listar usuarios activos <-")
        print("-> [4] Listar usuarios inactivos <-")
        print("-> [5] Actualizar usuario <-")
        print("-> [6] Eliminar usuario <-")
        print("-> [7] Buscar usuario <-")
        print("-> [8] Salir <-")

        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                crear_usuario()
            elif opcion == 2:
                listar_usuarios()
            elif opcion == 3:
                listar_usuarios(1)
            elif opcion == 4:
                listar_usuarios(0)
            elif opcion == 5:
                actualizar_usuario()
            elif opcion == 6:
                eliminar_usuario_logico()
            elif opcion == 7:
                buscar_usuario()
            elif opcion == 8:
                print("👋 Saliendo del programa.")
                break
            else:
                print("⚠️ Opción inválida.")
        except ValueError:
            print("⚠️ Entrada inválida. Por favor ingrese un número.")

menu_principal()