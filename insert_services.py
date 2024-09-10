from aesthetic_app import db, Service, app

# Establecer el contexto de la aplicación
with app.app_context():
    # Crear instancias de servicios
    service1 = Service(name="Tratamientos Corporales")
    service2 = Service(name="Tratamiento Facial")
    service3 = Service(name="Depilación")
    service4 = Service(name="Spa de Manos")
    service5 = Service(name="Masajes")
    service6 = Service(name="Gift Card")

    # Agregar los servicios a la sesión de la base de datos
    db.session.add(service1)
    db.session.add(service2)
    db.session.add(service3)
    db.session.add(service4)
    db.session.add(service5)
    db.session.add(service6)

    # Confirmar los cambios
    db.session.commit()

    print("Servicios insertados correctamente")

