'''
Created on Sep 3, 2012

@author: Edison Gustavo Muenz
'''
from organizer.mp3_organizer import fetch_songs, copy_songs, generate_filenames
import sys
import platform
import subprocess
import os

def main():
    filename = "playlist.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    if not os.path.exists(filename):
        if platform.system() == "Windows":
            with open("playlist.txt", 'w') as f:
                playlist_sample = \
r"""Zouk=c:\musicas\zouk\
Forro=c:\musicas\forro\
SambaLento=c:\musicas\Sambas\samba lento
SambaRapido=c:\musicas\Sambas\samba rapido

3 Zouk
2 Forro"""
                f.write(playlist_sample)
                f.close()
            subprocess.check_call("notepad playlist.txt", shell = True)
            filename = "playlist.txt"
        else:
            print("File %s does not exist" % filename)
            return

    print("Reading songs from %s " % filename)
    songs = fetch_songs(filename)
    copy_songs(generate_filenames(songs), 'output')

if __name__ == '__main__':
    main()
