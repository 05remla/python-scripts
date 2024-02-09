'''
    -o to file
    -p default if no args passed
    add -r for recurrsive
'''
import os
import sys
import hashlib
import argparse    
from hybrid_shell.hs import stringx
 
mainDict = dict()
sameFileArray = []
fileTrackerArray = []


class exclusion:
    def argParser():
        try:
            data = args.exclude
            sizeLimit = (int(data[1:]) * 1000000)
            if (data[0] == '<') or (data[0] == '>'):
                if (data[0] == '<'):
                    lessThan = True
                else:
                    lessThan = False
            else:
                raise
        
            exclusion.dict['data'] = [lessThan, sizeLimit]
        except:
            print('exclusion arg malformed. see help.')
            sys.exit()
    
    
    def fileParser(File):
        lessThan, sizeLimit = exclusion.dict['data']
        _pass = True
        fileSize = os.stat(File).st_size
        if lessThan:
            if (fileSize < sizeLimit):
                _pass = False
    
        else:
            if (fileSize > sizeLimit):
                _pass = False
    
        return(_pass)
                
        

def getFiles(RootDir):
    # RECURSIVE ON
    if args.recursive:
        for root, Dirs, Files in os.walk(RootDir):
            for FileName in Files:
                File = os.path.join(root, FileName).replace('\\', '/')
                yield(File)
    # RECURSIVE OFF
    else:
        for file in os.listdir(RootDir):
            File = os.path.join(RootDir, file).replace('\\', '/')
            if os.path.isfile(File):
                yield(File)
    
    
def run(RootDir):
    # BUILD HASH DICT
    print('building hash dictionary in memory...')
    PrevFile = ''

    for File in getFiles(RootDir):
        if args.exclude:
            if not exclusion.fileParser(File):
                continue
                
        print("\r{}".format(' ' * len(PrevFile)), end ="")
        print("\r{}".format(File), end ="")
        PrevFile = File
        try:
            hash = hashfile(File)
            mainDict[File] = hash
        except:
            pass

    print("\r{}".format(' ' * len(PrevFile)), end ="")
    print('\rCOMPLETE.')
    print()
                
    # FILE COMPARE PHASE
    indx = 0
    dictLen = len(mainDict)
    print("comparrison phase:")
    for i in mainDict.keys():
        indx += 1
        if i in fileTrackerArray:
            continue
            
        matchArray = [i]
        print("\r{} of {}".format(indx, dictLen), end ="")
        for j in mainDict.keys():
            if mainDict[i] == mainDict[j]:
                if not (i == j):
                    matchArray.append(j)
                    
        if (len(matchArray) > 1):
            sameFileArray.append(matchArray)
            for i in matchArray:
                fileTrackerArray.append(i)

    
    print()    
    # return(sameFileArray)

    
def command(cmd, File):
    stringx(cmd.format(File), True, True)
    
    
def hashfile(file):
    # A arbitrary (but fixed) buffer
    # size (change accordingly)
    # 65536 = 65536 bytes = 64 kilobytes
    BUF_SIZE = 65536
  
    # Initializing the sha256() method
    sha256 = hashlib.sha256()
  
    # Opening the file provided as
    # the first commandline argument
    with open(file, 'rb') as f:         
        while True:
            # reading data = BUF_SIZE from
            # the file and saving it in a
            # variable
            data = f.read(BUF_SIZE)
  
            # True if eof = 1
            if not data:
                break
      
            # Passing that data to that sh256 hash
            # function (updating the function with
            # that data)
            sha256.update(data)
  
      
    # sha256.hexdigest() hashes all the input
    # data passed to the sha256() via sha256.update()
    # Acts as a finalize method, after which
    # all the input data gets hashed hexdigest()
    # hashes the data, and returns the output
    # in hexadecimal format
    return sha256.hexdigest()
 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find duplicate files')
    parser.add_argument('-d', '--delete', action='store_true',
        help='delete all-but first found occurance of duplicate files')
    parser.add_argument('-cr', '--confirm', action='store_true',
        help='confirm action with user input for every file')
    parser.add_argument('-p', '--print', action='store_true',
        help='show/print duplicate files')
    parser.add_argument('-t', '--test', action='store_true',
        help='used in combination with --delete; won`t delete files. used for testing')
    parser.add_argument('-cd', '--command', type=str, nargs='?', 
        help='run command on file. use {} to denote file')
    parser.add_argument('-e', '--exclude', type=str, nargs='?', 
        help='string: starts with < or > followed immediatly by integer. [-e ">5"] = greater than 5Mb')
    parser.add_argument('-r', '--recursive', action='store_true', 
        help='run through all subdirecties')
    parser.add_argument('-o', '--outfile', type=str, nargs='?', 
        help='write duplicate file information to drive')
    args = parser.parse_args()

    if args.exclude:
        exclusion.dict = dict()
        exclusion.argParser()

    RootDir = input('starting directory: ')
    if not os.path.isdir(RootDir):
        print('{}: does not exist'.format(RootDir))
        sys.exit()
        
    run(RootDir)
        
    # DELETE seperated for file assurance
    # CLEANUP HERE
    if args.delete:
        for i in sameFileArray:
            for j in i[1:]:
                if args.confirm:
                    print()
                    yn = input('delete {}?: [Y/n]'.format(j))
                    if not ('n' in yn.lower()):
                        print('CONFIRMED, deleting {}...'.format(j))
                        if not args.test:
                            os.remove(j)
                else:
                    if args.print:
                        print('deleting {}...'.format(j))
                    if not args.test:
                        os.remove(j)

    elif args.outfile:
        outDir, outFile = os.path.split(args.outfile)
        if os.path.isdir(outDir):
            with open(args.outfile, 'w+') as openFile:
                for i in sameFileArray:
                    for j in i:
                        openFile.write('{}\n'.format(j))
                    openFile.write('\n')
                    
    else:
        for i in sameFileArray:
            shown = False
            for j in i:
                print(j)
                shown = True
                
            if args.command:
                for j in i:
                    if args.confirm:
                        print()
                        yn = input('run command on {}?: [Y/n]'.format(j))
                        if not ('n' in yn.lower()):
                            stringx(args.command.format(j), True, True)
                    else:
                        stringx(args.command.format(j), True, True)

            if shown:
                print()
        