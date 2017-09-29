import os
import flaskcrud
import unittest
import tempfile

class FlaskCRUDTestCase(unittest.TestCase):
    def setUp(self):
        # creates new test client and initializes new database
        # called before each individual test function is run
        self.db_fd, flaskcrud.app.config['DATABASE'] = tempfile.mkstemp()
        flaskcrud.app.testing = True
        self.app = flaskcrud.app.test_client()
        with flaskcrud.app.app_context():
            flaskcrud.flaskcrud.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskcrud.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password,
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_empty_db(self):
        rv = self.app.get('/') # GET request on application with given path
        assert b'No entries created yet' in rv.data

    def test_login_logout(self):
        rv = self.login('admin','default')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert b'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries created yet' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
    unittest.main()