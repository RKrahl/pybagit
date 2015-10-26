import unittest
import os
import os.path
import shutil
from pybagit.bagit import BagIt


class CreateExistingTest(unittest.TestCase):
    """ Create a bag with already existing data directory.
    """

    def setUp(self):
        self.bagdir = os.path.join(os.getcwd(), 'test', 'newtestbag')
        datadir = os.path.join(self.bagdir, 'data')
        datafile = os.path.join(os.getcwd(), 'test', 'testbag', 
                                'data', 'subdir', 'subsubdir', 'angry.jpg')
        os.mkdir(self.bagdir)
        os.mkdir(datadir)
        shutil.copy(datafile, datadir)

    def tearDown(self):
        if os.path.exists(self.bagdir):
            shutil.rmtree(self.bagdir)

    def test_bag_creation(self):
        newbag = BagIt(self.bagdir, create=True)
        newbag.update()
        self.assertTrue(os.path.exists(self.bagdir))
        self.assertTrue(os.path.exists(os.path.join(self.bagdir, 'bagit.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.bagdir, 'manifest-sha1.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.bagdir, 'data')))
        self.assertTrue(os.path.exists(os.path.join(self.bagdir, 'bag-info.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.bagdir, 'fetch.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.bagdir, 'tagmanifest-sha1.txt')))

        self.assertTrue(newbag.is_valid())
        self.assertEquals(newbag.manifest_contents[os.path.join('data', 'angry.jpg')],
                          u'c5913ae67aa40398f1182e52d2fa2c2e4c08f696')

def suite():
    test_suite = unittest.makeSuite(CreateExistingTest, 'test')
    return test_suite
