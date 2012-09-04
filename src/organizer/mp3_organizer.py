'''
Created on Sep 3, 2012

@author: Edison Gustavo Muenz
'''
import os
import collections
import random

class Entry(object):
    def __init__(self, label = None, quantity = None, path = None):
        '''
        @param label: str
        @param path: str
        @param quantity: int
        '''
        self.label = label
        if path is not None and not os.path.exists(path):
            raise RuntimeError("The directory " + path + " does not exist")
        self.path = path
        self.quantity = int(quantity)
        self.songs_list = []

    def __str__(self):
        return str((self.label, self.quantity, self.path))

class Playlist(object):
    '''
    Parses a playlist string without worrying about the real files
    '''
    def __init__(self, file_contents):
        '''
        @param filename: str
        '''
        self.entries = []

        self.__parse(file_contents.split("\n"))

    def __parse(self, lines):
        labels = dict()

        for line in lines:
            if line.strip() == "":
                continue

            tokens = line.split("=")
            if len(tokens) > 2:
                print("[warning] Ignoring the line " + line)
                continue

            tokens = [token.strip() for token in tokens]
            if len(tokens) == 2:

                # Specifying a label
                label = tokens[0]
                path = tokens[1]
                labels[label] = path

            else:
                tokens = tokens[0].split(" ")

                if len(tokens) != 2:
                    continue

                # Specifying a song entry
                label = tokens[1]
                quantity = int(tokens[0])
                self.entries.append(Entry(label, quantity))

        # now add the path to each entry
        for entry in self.entries:
            if entry.label not in labels:
                print("[warning] I couldn't find the label for '" + entry.label + "'. So I'm skipping this entry: " + str(entry))
                continue

            entry.path = labels[entry.label]

def pick_songs_from_available_files(playlist, available_files):
    '''
    @param playlist: Playlist
    @param dict("label" : ["filename1", "filename2" ...]
    @return list(string):
        The selected songs, randomized 
    '''
    songs = []
    files = dict(available_files)
    for entry in playlist.entries:
        label_files = set(files[entry.label])
        selected_files = random.sample(label_files, min(entry.quantity, len(label_files)))

        files[entry.label] = list(label_files.difference(selected_files))

        songs += selected_files

    return songs


def read_files_from_directory(input_dir, extensions = [".mp3", ".wma"]):
    '''
    Will scan @param(input_dir) recursively for files with any extension in @param(extensions).

    @param basedir: str
        The directory to look up the subdirectories
    @param subdirectories: list(str)
    @return: [filename1, filename2...]
    '''
    entries = []
    for dirname, dirnames, filenames in os.walk(input_dir):
        for filename in filenames:
            extension = os.path.splitext(filename)[1]
            if extension not in extensions:
                continue

            path = os.path.join(dirname, filename)
            path = os.path.normpath(path)
            entries.append(path)

    return entries


def __read_all_files(playlist):
    '''
    @param playlist:
    @type playlist: Playlist
    '''
    all_files = collections.defaultdict(list)
    for entry in playlist.entries:
        all_files[entry.label] = read_files_from_directory(entry.path)

    return all_files

def execute_and_fetch_songs(playlist_filename):
    playlist = Playlist(open(playlist_filename, 'r').read())
    all_files = __read_all_files(playlist)
    return pick_songs_from_available_files(playlist, all_files)
