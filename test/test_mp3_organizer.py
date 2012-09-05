'''
Created on Sep 3, 2012

@author: edison
'''
import unittest
from organizer.mp3_organizer import Playlist, read_files_from_directory, \
    pick_songs_from_available_files, fetch_songs, generate_filenames
import random
import os

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
        self.assertEqual("zouk", entry.label)
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
        self.assertEqual("zouk", entry.label)
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
        self.assertEqual("zouk", entry.label)
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
        self.assertEqual("zouk", entry.label)
        self.assertEqual(r"c:\Musicas\zouk", entry.path)

    def testLabel_Space_CaseInsensitive_IsTrimmed(self):
        organizer = Playlist(
r"""
3 Zouk Lento
2 Forro Rapido
5    Samba lento    

Zouk Lento=C:\Musicas\zouk lento
Forro rapido=C:\Musicas\Forro Rapido
 Samba lento = C:\Musicas\samba bem lento  
"""
                                 )
        self.assertEqual(3, len(organizer.entries))

        entry = organizer.entries[0]
        self.assertEqual(3, entry.quantity)
        self.assertEqual("zouk lento", entry.label)
        self.assertEqual(r"C:\Musicas\zouk lento", entry.path)

        entry = organizer.entries[1]
        self.assertEqual(2, entry.quantity)
        self.assertEqual("forro rapido", entry.label)
        self.assertEqual(r"C:\Musicas\Forro Rapido", entry.path)

        entry = organizer.entries[2]
        self.assertEqual(5, entry.quantity)
        self.assertEqual("samba lento", entry.label)
        self.assertEqual(r"C:\Musicas\samba bem lento", entry.path)



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
    def setUp(self):
        random.seed(0)

    def tearDown(self):
        random.seed()

    def testReadFilesFromDirectory(self):
        fetched_songs = read_files_from_directory(r"songs/zouk")
        self.assertItemsEqual(
                              [os.path.normpath("songs/zouk/zouk2.mp3"),
                               os.path.normpath("songs/zouk/zouk1.mp3")],
                              fetched_songs
                              )

    def testReadFilesFromDirectory_IsRecursive(self):
        fetched_songs = read_files_from_directory(r"songs/samba")
        self.assertItemsEqual(
                              [os.path.normpath("songs/samba/lento/samba_lento1.mp3"),
                               os.path.normpath("songs/samba/rapido/samba_rapido1.mp3")],
                              fetched_songs)

    def testReadFilesFromDirectory_DirectoryDoesNotExist(self):
        self.assertEqual(list(), read_files_from_directory("inexistent_dir"))
        self.assertEqual(list(), read_files_from_directory(""))

    def testFetchSongs(self):
        songs = fetch_songs("songs/playlist.txt")
        self.assertEqual(3, len(songs))

        self.assertItemsEqual(
                              [os.path.normpath("songs/zouk/zouk2.mp3"),
                               os.path.normpath("songs/zouk/zouk1.mp3")],
                              songs[0:2])
        self.assertEqual(os.path.normpath("songs/forro/forro1.mp3"), songs[2])

    def testGenerateFilenames(self):
        self.assertEqual([], generate_filenames([]))

        songs = ["song1.mp3", "dir1/song2.mp3", "dir2/song2.mp3"]
        self.assertEqual([("1 - song1.mp3", "song1.mp3"),
                          ("2 - dir1_song2.mp3", "dir1/song2.mp3"),
                          ("3 - dir2_song2.mp3", "dir2/song2.mp3")],
                         generate_filenames(songs))

        renamed_filenames = [renamed_filename for renamed_filename, _ in generate_filenames(songs)]
        self.assertEqual(["1 - song1.mp3", "2 - dir1_song2.mp3", "3 - dir2_song2.mp3"], sorted(renamed_filenames))

    def testGenerateFilenames_addPaddingZeroes(self):
        songs = generate_filenames(["song1.mp3"] * 100)
        self.assertEqual(("001 - song1.mp3", "song1.mp3"), songs[0])
        self.assertEqual(("002 - song1.mp3", "song1.mp3"), songs[1])
        self.assertEqual(("100 - song1.mp3", "song1.mp3"), songs[99])

    def testGenerateFilenames_commonPath(self):
        songs = [r"root\common_path\dir1\song1.mp3", "root\common_path\song2.mp3", "root\common_path\dir2\song2.mp3"]
        renamed_filenames = [renamed_filename for renamed_filename, _ in generate_filenames(songs)]
        self.assertEqual(["1 - dir1_song1.mp3", "2 - song2.mp3", "3 - dir2_song2.mp3"], renamed_filenames)

        songs = ["root/common_path/dir1/song1.mp3", "root/common_path/song2.mp3", "root/common_path/dir2/song2.mp3"]
        renamed_filenames = [renamed_filename for renamed_filename, _ in generate_filenames(songs)]
        self.assertEqual(["1 - dir1_song1.mp3", "2 - song2.mp3", "3 - dir2_song2.mp3"], renamed_filenames)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
