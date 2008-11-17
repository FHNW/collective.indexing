from unittest import defaultTestLoader
from collective.indexing.tests.base import IndexingTestCase
from collective.indexing.tests.layer import IndexingLayer
from collective.indexing.tests.utils import TestHelpers


# test-specific imports go here...
from transaction import commit
from collective.indexing.utils import isActive
from collective.indexing.monkey import setAutoFlush
from collective.indexing.config import AUTO_FLUSH


class AutoFlushTests(IndexingTestCase, TestHelpers):

    layer = IndexingLayer

    def afterSetUp(self):
        # clear logs to avoid id collisions
        setup = self.portal.portal_setup
        setup.manage_delObjects(setup.objectIds())

    def beforeTearDown(self):
        # reset to default
        setAutoFlush(AUTO_FLUSH)

    def testNoAutoFlush(self):
        # without auto-flush we must commit to update the catalog
        self.failUnless(isActive())
        setAutoFlush(False)
        self.assertEqual(self.create(), [])
        commit()
        self.assertEqual(self.fileIds(), ['foo'])
        self.assertEqual(self.remove(), ['foo'])
        commit()
        self.assertEqual(self.fileIds(), [])

    def testAutoFlush(self):
        # with auto-flush enabled the catalog is always up-to-date
        self.failUnless(isActive())
        setAutoFlush(True)
        # no commits required now
        self.assertEqual(self.create(), ['foo'])
        self.assertEqual(self.fileIds(), ['foo'])
        self.assertEqual(self.remove(), [])
        self.assertEqual(self.fileIds(), [])


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
