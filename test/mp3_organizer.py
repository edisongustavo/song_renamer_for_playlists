'''
Created on Sep 3, 2012

@author: edison
'''
import unittest
from organizer.mp3_organizer import Playlist, read_files_from_directory, \
    pick_songs_from_available_files, execute_and_fetch_songs
import random

class TestPlaylist(unittest.TestCase):

    def test(self):
        organizer = Playlist(
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
        organizer = Playlist(
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
        organizer = Playlist(
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
        organizer = Playlist(
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


class TestPickSongs(unittest.TestCase):

    def testPickSongsFromAvailableFiles(self):
        playlist = Playlist(r"""
song1=songs/song1/
song2=songs/song2/

1 song1
1 song2
""")
        available_files = {"song1" : ["songs/song1/song1.mp3"], "song2" : ["songs/song2/song2.mp3"]}

        mp3_list = pick_songs_from_available_files(playlist, available_files)
        self.assertListEqual(["songs/song1/song1.mp3", "songs/song2/song2.mp3"], mp3_list)

    def testPickSongsFromAvailableFiles_NotEnoughSongs(self):
        playlist = Playlist(r"""
song2=songs/song2
3 song2
""")
        available_files = {"song2" : ["songs/song2/song2.mp3"]}

        mp3_list = pick_songs_from_available_files(playlist, available_files)
        self.assertListEqual(["songs/song2/song2.mp3"], mp3_list)

    def testPickSongsFromAvailableFiles_DoesNotRepeatFile(self):
        playlist = Playlist(r"""
forro=songs/forro
zouk=songs/zouk
1 forro
1 zouk
1 forro
""")
        available_files = {"forro" : ["songs/forro/forro1.mp3", "songs/forro/forro2.mp3"], "zouk" : ["songs/zouk/zouk1.mp3"]}

        random.seed(0) #This seed makes it always sort the second item from the list
        mp3_list = pick_songs_from_available_files(playlist, available_files)
        self.assertListEqual(["songs/forro/forro1.mp3", "songs/zouk/zouk1.mp3", "songs/forro/forro2.mp3"], mp3_list)


class Test(unittest.TestCase):
    def testReadFilesFromDirectory(self):
        fetched_songs = read_files_from_directory(r"songs/zouk")
        self.assertEqual(["songs/zouk/zouk2.mp3", "songs/zouk/zouk1.mp3"], fetched_songs)

    def testReadFilesFromDirectory_IsRecursive(self):
        fetched_songs = read_files_from_directory(r"songs/samba")
        self.assertEqual(["songs/samba/lento/samba_lento1.mp3", "songs/samba/rapido/samba_rapido1.mp3"], fetched_songs)

    def testReadFilesFromDirectory_DirectoryDoesNotExist(self):
        self.assertEqual(list(), read_files_from_directory("inexistent_dir"))
        self.assertEqual(list(), read_files_from_directory(""))

    def testExecuteAndFetchSongs(self):
        random.seed(0)
        songs = execute_and_fetch_songs("songs/playlist.txt")
        self.assertEqual(["songs/zouk/zouk2.mp3", "songs/zouk/zouk1.mp3", "songs/forro/forro1.mp3"], songs)
        random.seed()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
