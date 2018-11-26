# services/users/project/tests/test_users.py

from project import db
from project.api.models import User

import json
import unittest

from project.tests.base import BaseTestCase


def add_user(nombre, apellidos, email, direccion, telefono, dni, ruc,
 fecha_nacimiento):
    user = User(nombre=nombre, apellidos=apellidos, email=email,
     direccion=direccion, telefono=telefono, dni=dni, ruc=ruc,
     fecha_nacimiento=fecha_nacimiento)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):

    def test_users(self):
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!!!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])

    def test_add_user(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'id': '2',
                    'nombre': 'zannier',
                    'apellidos': 'Vargas cisneros',
                    'email': 'zannier@gmail.com',
                    'direccion': 'Santa Eulalia',
                    'telefono': '961590878',
                    'dni': '40875698',
                    'ruc': '7894562369',
                    'fecha_nacimiento': '30/06/98'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                'zannier@gmail.com ha sido agregado!', data['mensaje'])
            self.assertIn('satisfactorio', data['estado'])

    def test_add_user_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_user_invalid_json_keys(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'abel.huanca@upeu.edu.pe'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_user_duplicate_email(self):
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'nombre': 'zannier',
                    'apellidos': 'Vargas cisneros',
                    'email': 'zannier@gmail.com',
                    'direccion': 'Santa Eulalia',
                    'telefono': '961590878',
                    'dni': '40875698',
                    'ruc': '7894562369',
                    'fecha_nacimiento': '30/06/98'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'nombre': 'zannier',
                    'apellidos': 'Vargas cisneros',
                    'email': 'zannier@gmail.com',
                    'direccion': 'Santa Eulalia',
                    'telefono': '961590878',
                    'dni': '40875698',
                    'ruc': '7894562369',
                    'fecha_nacimiento': '30/06/98'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Disculpe. Este email ya existe.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_user(self):
        user = add_user('zannier', 'Vargas cisneros', 'zannier@gmail.com',
        'Santa Eulalia', '961590878', '40875698', '7894562369', '30/06/98')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('zannier', data['data']['nombre'])
            self.assertIn('Vargas cisneros', data['data']['apellidos'])
            self.assertIn('zannier@gmail.com', data['data']['email'])
            self.assertIn('Santa Eulalia', data['data']['direccion'])
            self.assertIn('961590878', data['data']['telefono'])
            self.assertIn('40875698', data['data']['dni'])
            self.assertIn('7894562369', data['data']['ruc'])
            self.assertIn('30/06/98', data['data']['fecha_nacimiento'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_user_no_id(self):
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Usuario no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_user_incorrect_id(self):
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Usuario no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_all_users(self):
        add_user('zannier', 'Vargas cisneros', 'zannier@gmail.com',
         'Santa Eulalia', '961590878', '40875698', '7894562369', '30/06/98')
        add_user('Jesus', 'Chavez', 'jesus@gmail.com',
         'Inti', '961590878', '40875698', '123456', '31/07/98')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('zannier', data['data']['users'][0]['nombre'])
            self.assertIn(
                'Vargas cisneros', data['data']['users'][0]['apellidos'])
            self.assertIn(
                'zannier@gmail.com', data['data']['users'][0]['email'])
            self.assertIn(
                'Santa Eulalia', data['data']['users'][0]['direccion'])
            self.assertIn(
                '961590878', data['data']['users'][0]['telefono'])
            self.assertIn(
                '40875698', data['data']['users'][0]['dni'])
            self.assertIn(
                '30/06/98', data['data']['users'][0]['fecha_nacimiento'])

            self.assertIn(
                'Jesus', data['data']['users'][1]['nombre'])
            self.assertIn(
                'Chavez', data['data']['users'][1]['apellidos'])
            self.assertIn(
                'jesus@gmail.com', data['data']['users'][1]['email'])
            self.assertIn(
                'Inti', data['data']['users'][1]['direccion'])
            self.assertIn(
                '961590878', data['data']['users'][1]['telefono'])
            self.assertIn(
                '40875698', data['data']['users'][1]['dni'])
            self.assertIn(
                '123456', data['data']['users'][1]['ruc'])
            self.assertIn(
                '31/07/98', data['data']['users'][1]['fecha_nacimiento'])

            self.assertIn('satisfactorio', data['estado'])


if __name__ == '__main__':
    unittest.main()