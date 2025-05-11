import unittest
from unittest.mock import patch, MagicMock
from flask import json
from uuid import uuid4
from app import create_app, db 
from app.models.blacklist import BlacklistEntry
from app.schemas.blacklist import BlacklistSchema

class BlacklistResourceTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        self.app.config['STATIC_BEARER_TOKEN'] = 'test_token'
        self.client = self.app.test_client()

        with self.app.app_context():
            self.db = db
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_get_blacklists_authenticated(self):
        with self.app.app_context():
            entry1 = BlacklistEntry(email='test1@example.com', app_uuid=uuid4(), blocked_reason='razon1', ip_address='127.0.0.1')
            entry2 = BlacklistEntry(email='test2@example.com', app_uuid=uuid4(), blocked_reason='razon2', ip_address='127.0.0.1')
            self.db.session.add_all([entry1, entry2])
            self.db.session.commit()

        response = self.client.get('/api/v1/blacklists', headers={'Authorization': 'Bearer test_token'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('blacklists', data)
        self.assertEqual(len(data['blacklists']), 2)

    def test_get_blacklists_unauthenticated(self):
        response = self.client.get('/api/v1/blacklists')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Token invalido')

    
    def test_post_blacklist_authenticated_invalid_email(self):
        response = self.client.post('/api/v1/blacklists', json={
            'email': 'invalid-email',
            'app_uuid': str(uuid4()),
            'blocked_reason': 'Razón de prueba'
        }, headers={'Authorization': 'Bearer test_token'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('email', data)

    def test_post_blacklist_authenticated_email_already_exists(self):
        with self.app.app_context():
            existing_entry = BlacklistEntry(email='exists@example.com', app_uuid=uuid4(), blocked_reason='razon', ip_address='127.0.0.1')
            self.db.session.add(existing_entry)
            self.db.session.commit()

        response = self.client.post('/api/v1/blacklists', json={
            'email': 'exists@example.com',
            'app_uuid': str(uuid4()),
            'blocked_reason': 'Otra razón'
        }, headers={'Authorization': 'Bearer test_token'})
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Email exists@example.com ya se encuentra en la blacklist')

    def test_post_blacklist_unauthenticated(self):
        response = self.client.post('/api/v1/blacklists', json={
            'email': 'new@example.com',
            'app_uuid': str(uuid4()),
            'blocked_reason': 'Razón de prueba'
        })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Token invalido')

    @patch('app.views.blacklist.db.session.commit')
    def test_post_blacklist_authenticated_db_error(self, mock_commit):
        mock_commit.side_effect = Exception("Database error")

        response = self.client.post('/api/v1/blacklists', json={
            'email': 'db_error@example.com',
            'app_uuid': str(uuid4()),
            'blocked_reason': 'Razón de prueba'
        }, headers={'Authorization': 'Bearer test_token'})
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Internal server error while adding email')        
        
    #def test_fallo_simulado_para_entrega(self):
    #    self.assertFalse(True, "Fallo simulado para ver el pipeline fallar")

class BlacklistDetailResourceTests(unittest.TestCase):

    def setUp(self):
        # Crea la aplicación directamente aquí
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['STATIC_BEARER_TOKEN'] = 'test_token'
        self.client = self.app.test_client()

        with self.app.app_context():
            self.db = db
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_get_blacklist_detail_authenticated_found(self):
        with self.app.app_context():
            entry = BlacklistEntry(email='findme@example.com', app_uuid=uuid4(), blocked_reason='Razón encontrada', ip_address='127.0.0.1')
            self.db.session.add(entry)
            self.db.session.commit()

        response = self.client.get('/api/v1/blacklists/findme@example.com', headers={'Authorization': 'Bearer test_token'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['is_blacklisted'], True)
        self.assertEqual(data['blocked_reason'], 'Razón encontrada')

    def test_get_blacklist_detail_authenticated_not_found(self):
        response = self.client.get('/api/v1/blacklists/notfound@example.com', headers={'Authorization': 'Bearer test_token'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['is_blacklisted'], False)
        self.assertIsNone(data['blocked_reason'])

    def test_get_blacklist_detail_unauthenticated(self):
        response = self.client.get('/api/v1/blacklists/any@example.com')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Token invalido')


if __name__ == '__main__':
    unittest.main()