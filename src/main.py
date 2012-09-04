'''
Created on Sep 3, 2012

@author: Edison Gustavo Muenz
'''
from organizer.mp3_organizer import execute_and_fetch_songs
import sys
import platform
import subprocess

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
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
            retcode = subprocess.check_call("notepad playlist.txt", shell = True)
            print("Command completed! Retcode: %i " % retcode)
            filename = "playlist.txt"
            return
        else:
            print("Usage: %s <playlist_file>" % sys.argv[0])
            return

    songs = execute_and_fetch_songs(filename)
    for song in songs:
        print(song)

if __name__ == '__main__':
    main()
