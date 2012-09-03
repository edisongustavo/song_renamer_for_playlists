'''
Created on Sep 3, 2012

@author: Edison Gustavo Muenz
'''
from organizer.mp3_organizer import Mp3Organizer
import os

if __name__ == '__main__':
    organizer = Mp3Organizer(open("arquivos.txt", 'r').read_lines())
    
    output_dir = "folder"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    organizer.copy_to_folder(output_dir)
