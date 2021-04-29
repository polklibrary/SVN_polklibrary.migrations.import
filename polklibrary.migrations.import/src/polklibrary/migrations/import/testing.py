# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import polklibrary.migrations.import


class PolklibraryMigrationsImportLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=polklibrary.migrations.import)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'polklibrary.migrations.import:default')


POLKLIBRARY_MIGRATIONS_IMPORT_FIXTURE = PolklibraryMigrationsImportLayer()


POLKLIBRARY_MIGRATIONS_IMPORT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(POLKLIBRARY_MIGRATIONS_IMPORT_FIXTURE,),
    name='PolklibraryMigrationsImportLayer:IntegrationTesting',
)


POLKLIBRARY_MIGRATIONS_IMPORT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(POLKLIBRARY_MIGRATIONS_IMPORT_FIXTURE,),
    name='PolklibraryMigrationsImportLayer:FunctionalTesting',
)


POLKLIBRARY_MIGRATIONS_IMPORT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        POLKLIBRARY_MIGRATIONS_IMPORT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='PolklibraryMigrationsImportLayer:AcceptanceTesting',
)
