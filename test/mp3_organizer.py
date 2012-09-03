'''
Created on Sep 3, 2012

@author: edison
'''
import unittest
from organizer.mp3_organizer import Mp3Organizer


class Test(unittest.TestCase):

    def testMp3Organizer(self):
        organizer = Mp3Organizer(
r"""
Zouk=c:\Musicas\zouk
Salsa=C:\Musicas\salsa
Samba=C:\Musicas\samba

3 Zouk
2 Salsa
3 Samba
"""
                                 )
        self.assertEqual(3, len(organizer.entries))
        entry = organizer.entries[0]
        self.assertEqual(3, entry.quantity)
        self.assertEqual("Zouk", entry.label)
        self.assertEqual(r"c:\Musicas\zouk", entry.path)
        
    def testSpecifyLabelsAfterSonglist(self):
        organizer = Mp3Organizer(
r"""
3 Zouk
2 Salsa
3 Samba

Zouk=c:\Musicas\zouk
Salsa=C:\Musicas\salsa
Samba=C:\Musicas\samba
"""
                                 )
        self.assertEqual(3, len(organizer.entries))
        entry = organizer.entries[0]
        self.assertEqual(3, entry.quantity)
        self.assertEqual("Zouk", entry.label)
        self.assertEqual(r"c:\Musicas\zouk", entry.path)
        
    def testLabelAppearMoreThanOnce(self):
        organizer = Mp3Organizer(
r"""
3 Zouk
2 Forro
5 Zouk

Zouk=c:\Musicas\zouk
Forro=C:\Musicas\forro
"""
                                 )
        self.assertEqual(3, len(organizer.entries))
        entry = organizer.entries[0]
        self.assertEqual(3, entry.quantity)
        self.assertEqual("Zouk", entry.label)
        self.assertEqual(r"c:\Musicas\zouk", entry.path)
        
    def testExtraLabel(self):
        organizer = Mp3Organizer(
r"""
3 Zouk
2 Forro
5 Zouk

Zouk=c:\Musicas\zouk
Forro=C:\Musicas\Forro
Samba=C:\Musicas\samba
"""
                                 )
        self.assertEqual(3, len(organizer.entries))
        entry = organizer.entries[0]
        self.assertEqual(3, entry.quantity)
        self.assertEqual("Zouk", entry.label)
        self.assertEqual(r"c:\Musicas\zouk", entry.path)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
