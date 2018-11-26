# services/users/manage.py 


import unittest

from flask.cli import FlaskGroup

from project import create_app, db   # <-- nuevo
from project.api.models import User


app = create_app()
cli = FlaskGroup(create_app=create_app)  # <-- nuevo


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Ejecuta las pruebas sin cobertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def seed_db():
    db.session.add(User(nombre='Zannier', apellidos="Vargas Cisneros",
        email="aza@gmail.com", direccion="Lima", telefono="961590878",
        dni="75053012", ruc="ruc",
        fecha_nacimiento="30-06-98"))
    db.session.commit()


if __name__ == '__main__':
    cli()
