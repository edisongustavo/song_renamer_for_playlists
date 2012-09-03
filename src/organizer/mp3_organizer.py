'''
Created on Sep 3, 2012

@author: Edison Gustavo Muenz
'''
import os

class Entry(object):
    def __init__(self, label=None, quantity=None, directory_path=None):
        '''
        @param label: str
        @param path: str
        @param quantity: int
        '''
        self.label = label
        if directory_path is not None and not os.path.exists(directory_path):
            raise RuntimeError("The directory " + directory_path + " does not exist")
        self.path = directory_path
        self.quantity = int(quantity)
        
    def __str__(self):
        return str((self.label, self.quantity, self.path))
    
class Mp3Organizer(object):
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
