"""These are the class definitions for basic test cases, used by unittest.
Add to them as you see fit."""

import unittest
import os
import main
from app import create_app


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['APP_ENV'] = 'test'

    def tearDown(self):
        os.environ.pop('APP_ENV')

    def test_main_is_running(self):
        self.assertTrue(main.main())

    def test_app_is_not_none(self):
        self.assertTrue(create_app("") is not None)

    def test_logger_is_present(self):
        self.assertLogs()

    def test_config_is_not_empty(self):
        from pathlib import Path
        from configparser import RawConfigParser

        root = Path('.') / os.getcwd()
        cfg_path = root / 'config' / '{}.ini'.format(os.environ.get('APP_ENV'))
        cfg_parser = RawConfigParser()
        cfg = cfg_parser.read(cfg_path)
        self.assertTrue(len(cfg) > 0)
