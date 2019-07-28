# This file is part of Chatlog Search
# Copyright (C) 2019 QueenPengu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public Licensse as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http:\\www.gnu.org\licenses\>.

import os, re, time
from configparser import ConfigParser
from gzip import open as opengz


def main():
    # Show GNU information
    gnu()
    
    # Open config file and get settings
    useRegex, debug, path = config()

    # Display search type
    if debug:
        if useRegex:
            print("Search type: Regex")
        else:
            print("Search type: Text")

    # Get input            
    searchTerm = input("Enter a search string:\n>")
    print("Searching...")

    # Search logs
    results = search(path, useRegex, searchTerm, debug)

    # Write to txt file
    filename = "ResultsFor_{}.txt".format(re.sub(r"\W+", "", searchTerm))          
    writeFile(filename, results, debug)

    if debug:
        input("Done.\n\nPress enter to view results.\n")

    return filename


def gnu():
    print("""Chatlog Search v1.4 Copyright (C) 2019 QueenPengu
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions (see LICENSE.txt for more information).
""")


def config():
    config = ConfigParser()
    
    if os.path.isfile("search_config.ini"):
        # Read config file
        config.read("search_config.ini")

        try:
            useRegex = config.getboolean("settings", "use regex")
            debug = config.getboolean("settings", "debug")
            path = config.get("settings", "logs folder")
            return useRegex, debug, path
        
        except Exception as ex:
            # Couldn't read values
            print(ex)
            input("There was an error in search_config.ini\nEither fix the error or delete search_config.ini to generate a new one with default settings.\n\nPress enter to exit.\n")
            exit()
        
    else:
        # Create config file
        print("No config file found.")
        
        config["settings"] = {
            "use regex": "off",
            "debug": "on",
            "logs folder": os.path.expandvars("%APPDATA%\\.minecraft\\logs\\")
            }
        with open("search_config.ini", "w") as file:
            config.write(file)

        print("search_config.ini created with the following settings:\nuse regex = {}\ndebug = {}\nlogs folder = {}\n"
              .format(config["settings"]["use regex"],
                      config["settings"]["debug"],
                      config["settings"]["logs folder"]))
            
        return False, True, config["settings"]["logs folder"]


def search(d, useRegex, searchTerm, debug):
    results = []
    
    for file in os.listdir(d):
        filepath = str(d + file)
            
        if file.endswith('.log'):
            # Read plain text
            if debug:
                print("Searching: {}".format(file))

            with open(filepath, 'r') as contents:
                for line in contents:
                    if useRegex:
                        if re.search(searchTerm, line):
                            results.append(str(file + line))
                    else:
                        if searchTerm in line.lower():
                            results.append(str(file + line))
                            
        elif file.endswith('.log.gz'):
            # Read compressed text
            if debug:
                print("Searching: {}".format(file))
                
            try:
                with opengz(filepath, 'rt') as contents:
                    for line in contents:
                        if useRegex:
                            if re.search(searchTerm, line):
                                results.append(str(file + line))
                        else:
                            if searchTerm in line.lower():
                                results.append(str(file + line))
                            
            except EOFError:
                # Catch for missing end of file marker
                if debug:
                    print("\nEOFError: {} ended before the end-of-stream marker was reached\n".format(file))
        elif debug:
            # Show skipped files
            print("File Skipped: {}".format(file))

    return results


def writeFile(filename, results, debug):
    if debug:
        print("Writing to file: {}".format(filename))
        
    with open(filename, "w") as file:
        for line in results:
            file.write(line)


# Open results file and shut console
path = str(os.getcwd() + "\\" + main())
os.system("start " + path)
exit()
