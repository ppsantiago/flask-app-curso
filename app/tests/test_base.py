from flask import current_app, url_for
from flask_testing import TestCase
from main import app

class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        # app.config['SERVER_NAME'] = '127.0.0.1:5000'
        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)


    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])


    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertStatus(response, 302)        
        
        
    def test_inicio_get(self):
        response = self.client.get(url_for('inicio'))
        self.assert200(response)

        
    def test_hello_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }
        response = self.client.post(url_for('inicio'), data=fake_form)
        self.assertStatus(response, 302)
        
    def test_auth_blooprint_exist(self):
        self.assertIn('auth', self.app.blueprints)
        
    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)


    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assert_template_used('auth/login.html')
