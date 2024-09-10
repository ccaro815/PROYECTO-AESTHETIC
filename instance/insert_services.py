from aesthetic_app import db, Service, app

with app.app_context():

    service1 = Service(name="Tratamientos Corporales")
    service2 = Service(name="Tratamiento Facial")
    service3 = Service(name="Depilación")
    service4 = Service(name="Spa de Manos")
    service5 = Service(name="Masajes")
    service6 = Service(name="Gift Card")

    db.session.add(service1)
    db.session.add(service2)
    db.session.add(service3)
    db.session.add(service4)
    db.session.add(service5)
    db.session.add(service6)

    # Confirmar los cambios
    db.session.commit()

    print("Servicios insertados correctamente")