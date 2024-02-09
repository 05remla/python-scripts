#!/usr/bin/python3
'''
    TO-DO: 
        [X] move recurssive finder and local finder into manager and reduce number of functions
        [X] use sys.stdout so data is available outside interpreter
        [/] returning double files : temp fix with reported list var
        [ ] MAKE HELP FUNCTION
        [ ] arg and switch work
        [ ] decoding files when reading
        
    SWITCHES:
    -r
    -ret
    -no
    --update_method=file
    --search_words=word1,word_two
    --update_file=/home/words.txt
    
    VARIABLE ORDER FOR ALL FUNCTIONS (WHEN IMPORTED AS LIBRARY):
    1. file or dir : string
    2. recursive   : bool
    2. name only   : bool
    3. return      : bool

    LIBRARY USAGE:
    xx = fileSifterMain.manager('/home/leo/Documents', recursive=True, ret=True)
    for i in xx:
        print(i[0])
        for j in i[1]:
            print(j)
        print()
        
    --- same as ---
    
    SCRIPT USAGE:
    python docsSearch.py -r -ret /home/leo/Documents
    
    --- also ---
    python3 docsSearch.py -r --update_method=overwrite --search_words=__main__ /home/leo/
'''
import os
import sys
from colorama import Back, Fore, Style

c1 = Fore.GREEN + Style.BRIGHT
c2 = Fore.BLACK + Style.BRIGHT
_r = Style.RESET_ALL

variable_dict = {'-r': False, '-ret': False, '-no': False}
variable_dict['search_list'] = [' pass ', 'password', 'username', 'email', 'login', ' phrase',
                                ' secret', ' pin', 'client', ' creds', 'credential']

variable_dict['update_method'] = None

class fileSifterMain():
    class textSearch():
        def search(FILE, ret=variable_dict['-r']):
            if (ret == None):
                ret = variable_dict['-ret']
                
            if os.path.isfile(FILE):
                try:
                    _return = []
                    data = []
                    with open(FILE) as openFile:
                        for line in openFile.readlines():
                            data.append(line.strip())
                            
                    line_indx = 0
                    for j in data:
                        line_indx += 1
                        for k in variable_dict['search_list']:
                            if (k.lower() in j.lower()):
                                structured_line = 'line {}. {}'.format(line_indx, j)
                                if not (structured_line in _return):
                                    _return.append('line {}. {}'.format(line_indx, j))
                                
                    if ret:
                        if (len(_return) == 0):
                            _return = False
                        return(_return)
                    else:
                        for i in _return:
                            sys.stdout.write('{}\n'.format(i))
                except:
                    return(False)
            
        def iterSearch(files):
            for _file in files:
                name = _file                
                data = [name]
                search_return = fileSifterMain.textSearch.search(name,True)
                if not (search_return == False) and not (search_return == None):
                    data.append(search_return)
                    yield(data)
                
    def recursiveFileFinder(DIR, ret=variable_dict['-ret']):
        fileNames = []
        for root, dirs, files in os.walk(DIR):            
            for file in files:
                fileNames.append(os.path.join(root, file))
        #print(fileNames)
        for i in fileSifterMain.textSearch.iterSearch(fileNames):
            yield(i)            
                                
    def localFileFinder(DIR, ret=variable_dict['-ret']):
        reported = []
        files = []
        finder_return = []
        for file in os.listdir(DIR):
            if os.path.isfile(file):
                files.append(file)
                
        for i in fileSifterMain.textSearch.iterSearch(files):
            finder_return.append(i)            
        return(finder_return)
    
    def manager(DIR, recursive=variable_dict['-r'], nameOnly=variable_dict['-no'], ret=variable_dict['-ret']):
        _return = []            
        if recursive:
            finder_return = []
            for i in fileSifterMain.recursiveFileFinder(DIR, ret):
                finder_return.append(i)
        else:
            finder_return = fileSifterMain.localFileFinder(DIR, ret)
            
        for i in finder_return:
            if ret:
                if nameOnly:
                    _return.append(i[0])
                else:
                    _return.append(i)
            else:
                sys.stdout.write('{}{}{}:\n'.format(c1,i[0],_r))
                if not nameOnly:
                    for j in i[1]:
                        sys.stdout.write('{}\n'.format(j))
                    sys.stdout.write('\n')
                
        if ret:
            return(_return)

            
if __name__ == "__main__":
    args = sys.argv[1:]
    isDir = False
    isFile = False


    def updateTextSearchList():
        if (variable_dict['update_method'] == None):
            pass
        elif (variable_dict['update_method'] == 'file'):
            if os.path.isfile(variable_dict['update_file']):
                variable_dict['search_list'] = []
                with open(variable_dict['update_file']) as openFile:
                    for line in openFile.readlines():
                        variable_dict['search_list'].append(line.strip())
        elif (variable_dict['update_method'] == 'add'):
            for i in variable_dict['search_words'].split(','):
                variable_dict['search_list'].append(i)
        elif (variable_dict['update_method'] == 'overwrite'):
            variable_dict['search_list'] = []
            for i in variable_dict['search_words'].split(','):
                variable_dict['search_list'].append(i)

    
    def printHelp():
        help_string = '''** content_searcher **
    searches contents of file for key words by specifying individual files or 
    directories. Capable of batch searching individual directories and 
    recursivly searching directory trees.
     
    ARGS:
        SWITCHES:
            -h   : print help and usage information
            -r   : recursive directory search
            -ret : return output instead of printing (internal to python?)
            -no  : list filenames only, not contents

        KEY VALUE ARGS (ADVANCED):
            --search_words=word1,word_two : search words definition (no spaces)
            --update_file=/home/words.txt : file to be used to define search words (one word per line)
            --update_method=${method}     : search word update method [default: add]
                                            *methods are: [file, add, overwrite]
                                            
    DEFAULT SEARCH WORDS:
        [' pass ', 'password', 'username', 'email', 'login', ' phrase',
         ' secret', ' pin', 'client', ' creds', 'credential']
    
    USAGE:
    python docsSearch.py -r -no /home/user
    python3 docsSearch.py -r --update_method=overwrite --search_words=credential /home/user/
    python3 docsSearch.py -r --search_words=poison /home/user/
        '''
        
        print(help_string)
        exit()

        
    if (len(args) > 0):
        if os.path.isdir(args[-1]):
            isDir = True
        elif os.path.isfile(args[-1]):
            isFile = True
            
        # CHECK FOR HELP SWITCH FIRST
        for i in range(len(args)):
            if (args[i] == '-h'):
                printHelp()
                
        # CHECK REMAINING ARGS
        for i in range(len(args)):
            # switches are named in variableDictionary as
            # themselves for easy updating
            if (args[i] in variable_dict.keys()):
                variable_dict[args[i]] = True
            elif (args[i].startswith('--')):
                # search_list updating
                # options: append, overwrite, file import
                key,value = args[i].split('=')
                key = key[2:]
                variable_dict[key] = value
            else:
                if not (i == len(args)):
                    print('switch: {}, not understood'.format(args[i]))
                    printHelp()
    
        # IF ADDITIONAL WORDS PROVIDED WITH NO UPDATE METHOD: JUST APPEND
        if ('search_words' in variable_dict.keys()):
            if (variable_dict['update_method'] == None):
                variable_dict['update_method'] = 'add'
                
        updateTextSearchList()
        
        if isFile:
            fileSifterMain.textSearch.search(args[-1])
        elif isDir:
            fileSifterMain.manager(args[-1], variable_dict['-r'], variable_dict['-no'], variable_dict['-ret'])
    else:
        printHelp()
    