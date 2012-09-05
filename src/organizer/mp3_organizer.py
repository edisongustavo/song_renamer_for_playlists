'''
Created on Sep 3, 2012

@author: Edison Gustavo Muenz
'''
import os
import collections
import random
import math
import shutil

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
            line = line.strip()
            if line == "":
                continue

            if '=' in line:
                # Specifying a label
                label, _, path = line.partition('=')
                label = label.strip().lower()
                labels[label] = path.strip()

            elif ' ' in line:
                # Specifying a song entry
                quantity, _, label = line.partition(" ")
                quantity = int(quantity)
                label = label.strip().lower()
                self.entries.append(Entry(label, quantity))
            else:
                print("[warning] Ignoring the line %s" % line)

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
    for dirname, _, filenames in os.walk(input_dir):
        for filename in filenames:
            extension = os.path.splitext(filename)[1]
            if extension not in extensions:
                continue

            path = os.path.join(dirname, filename)
            path = os.path.normpath(path)
            entries.append(path)

    return entries

def generate_filenames(filenames):
    '''
    Generates a list of tuples like this: (ordered_name, original_filename).
    The ordered_name is like this so that when sorting this list alphabetically,
    the names will be kept in the same order
     
    @param filenames: [string]
    @return [(string, string)]
    '''
    if len(filenames) == 0:
        return []

    filenames = [os.path.normpath(f) for f in filenames]

    common_path = os.path.commonprefix(filenames)

    #The common path might be referring to a file (in case all filenames are equal)
    if os.path.splitext(common_path)[1] != '':
        common_path = os.path.split(common_path)[0]

    #do actual renaming
    renamed_filenames = []
    padding_zeroes = int(math.floor(math.log(len(filenames), 10))) + 1 #taken from: http://www.mathpath.org/concepts/Num/numdigits.htm
    for i in xrange(len(filenames)):
        renamed_filename = str(i + 1).zfill(padding_zeroes) + " - "
        p = filenames[i]
        p = p.replace(common_path, '', 1)
        p = p.replace("\\", '_')
        p = p.replace("/", '_')
        renamed_filename += p

        renamed_filenames.append((renamed_filename, filenames[i]))

    return renamed_filenames

def __read_all_files(playlist):
    '''
    @param playlist:
    @type playlist: Playlist
    '''
    all_files = collections.defaultdict(list)
    for entry in playlist.entries:
        all_files[entry.label] = read_files_from_directory(entry.path)

    return all_files

def fetch_songs(playlist_filename):
    playlist = Playlist(open(playlist_filename, 'r').read())
    all_files = __read_all_files(playlist)
    return pick_songs_from_available_files(playlist, all_files)

def copy_songs(filenames, output_dirname):
    '''
    Copies to the @param(output_dirname) all the files from @param(filenames)
    
    @param filenames: [(string, string)] -> (destiny_filename, original_filename)
    @param output_dirname: string
    '''
    if len(filenames) == 0:
        return

    if not os.path.exists(output_dirname):
        os.mkdir(output_dirname)

    total_copied = 0
    for file_to, file_from in filenames:
        size = os.path.getsize(file_from)
        total_copied += size
        print("{0:.1f} MB Copying the file '{1}'".format(size / 1024.0 / 1024.0, os.path.basename(file_from)))
        shutil.copy2(file_from, os.path.join(output_dirname, file_to))
