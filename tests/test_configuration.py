import os
import sys
import unittest
from unittest.mock import patch

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nextcloud_service_reminder import load_configuration, initialize_configuration, validate_config, CONFIG

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        # Backup original environ
        self._old_environ = dict(os.environ)

    def tearDown(self):
        # Restore environ
        os.environ.clear()
        os.environ.update(self._old_environ)
        # Clear CONFIG to avoid cross-test contamination
        import nextcloud_service_reminder
        nextcloud_service_reminder.CONFIG = None

    def test_load_configuration_success(self):
        test_env = {
            'CALDAV_URL': 'https://test.nextcloud.example/nextcloud/',
            'CALDAV_USER': 'testuser',
            'CALDAV_PASSWORD': 'testpass',
            'WHATSAPP_API_URL': 'https://api.whatsapp.com/v1/',
            'WHATSAPP_API_TOKEN': 'testtoken',
            'LOG_LEVEL': 'DEBUG'
        }
        with patch.dict(os.environ, test_env, clear=True):
            config = load_configuration()
            self.assertEqual(config['caldav_url'], 'https://test.nextcloud.example/nextcloud/')
            self.assertEqual(config['caldav_user'], 'testuser')
            self.assertEqual(config['caldav_password'], 'testpass')
            self.assertEqual(config['whatsapp_api_url'], 'https://api.whatsapp.com/v1/')
            self.assertEqual(config['whatsapp_api_token'], 'testtoken')
            self.assertEqual(config['log_level'], 'DEBUG')

    def test_load_configuration_missing_vars(self):
        test_env = {
            'CALDAV_URL': 'https://test.nextcloud.example/nextcloud/',
            # missing CALDAV_USER etc
        }
        with patch.dict(os.environ, test_env, clear=True):
            with self.assertRaises(EnvironmentError) as cm:
                load_configuration()
            self.assertIn('Missing required environment variables', str(cm.exception))

    def test_initialize_configuration_sets_global(self):
        test_env = {
            'CALDAV_URL': 'https://test.nextcloud.example/nextcloud/',
            'CALDAV_USER': 'testuser',
            'CALDAV_PASSWORD': 'testpass',
            'WHATSAPP_API_URL': 'https://api.whatsapp.com/v1/',
            'WHATSAPP_API_TOKEN': 'testtoken',
        }
        with patch.dict(os.environ, test_env, clear=True):
            initialize_configuration()
            # CONFIG should now be set
            from nextcloud_service_reminder import CONFIG
            self.assertIsNotNone(CONFIG)
            self.assertEqual(CONFIG['caldav_url'], 'https://test.nextcloud.example/nextcloud/')

    def test_validate_config_success(self):
        test_env = {
            'CALDAV_URL': 'https://test.nextcloud.example/nextcloud/',
            'CALDAV_USER': 'testuser',
            'CALDAV_PASSWORD': 'testpass',
            'WHATSAPP_API_URL': 'https://api.whatsapp.com/v1/',
            'WHATSAPP_API_TOKEN': 'testtoken',
        }
        with patch.dict(os.environ, test_env, clear=True):
            initialize_configuration()
            # Should not raise
            try:
                validate_config()
            except Exception:
                self.fail("validate_config raised an exception unexpectedly!")

    def test_validate_config_missing_key(self):
        test_env = {
            'CALDAV_URL': 'https://test.nextcloud.example/nextcloud/',
            'CALDAV_USER': 'testuser',
            'CALDAV_PASSWORD': 'testpass',
            'WHATSAPP_API_URL': 'https://api.whatsapp.com/v1/',
            # missing WHATSAPP_API_TOKEN
        }
        with patch.dict(os.environ, test_env, clear=True):
            initialize_configuration()
            with self.assertRaises(EnvironmentError):
                validate_config()

if __name__ == '__main__':
    unittest.main()