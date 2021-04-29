# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from polklibrary.migrations.import.testing import POLKLIBRARY_MIGRATIONS_IMPORT_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that polklibrary.migrations.import is properly installed."""

    layer = POLKLIBRARY_MIGRATIONS_IMPORT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if polklibrary.migrations.import is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'polklibrary.migrations.import'))

    def test_browserlayer(self):
        """Test that IPolklibraryMigrationsImportLayer is registered."""
        from polklibrary.migrations.import.interfaces import (
            IPolklibraryMigrationsImportLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IPolklibraryMigrationsImportLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = POLKLIBRARY_MIGRATIONS_IMPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['polklibrary.migrations.import'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if polklibrary.migrations.import is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'polklibrary.migrations.import'))

    def test_browserlayer_removed(self):
        """Test that IPolklibraryMigrationsImportLayer is removed."""
        from polklibrary.migrations.import.interfaces import \
            IPolklibraryMigrationsImportLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IPolklibraryMigrationsImportLayer,
            utils.registered_layers())
