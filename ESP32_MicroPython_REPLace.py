#!/usr/bin/python3

# ----------------------------------------------------------------------------------

# replace.py = REPLace.py = REPL Ace Uploder
# Copyright (c) 2017 Clayton Darwin
# claytondarwin.com claytondarwin@gmail.com

# This uses a serial connection to REPL to copy dirs/files to a MicroPython instance.
# This is slow. It's just auto-writing Python commands to the REPL connection.
# I've only tested this on Debian Linux, but it should work other places.

# This REQUIRES the pyserial module: sudo pip3 install pyserial
# Add your username to dialout: sudo adduser username dialout
# You have to log out and back in or reboot after changing dialout.
# Now just set the port:

port = '/dev/ttyUSB0'

# Given a local folder using the variable file_system_dir,
# this overwrites the folder content to the flash of the MicroPython instance.
# The file_system_dir folder becomes the root directory on the chip.
# If file_system_dir is None, it will use the current working directory. 

file_system_dir = None

# Any directory or file whose basename matches an item in "excludes"
# will not be copied to the MicroPython instance. So, you can run this
# script from the file_system_dir folder.

excludes = ['REPLace.py','archive']

# This is the opposite of excludes. If you list basenames here, then only
# matches to these basenames will be loaded. You can use this if you are
# editing only a few files. Note that the subdir names must be included
# here if you want to walk into subdirs.

includes = ['main.py','npxy.py','nettools.py','clock1.py','clock2.py']

# The following variable reduces upload size.
# If True, this removes blank lines, comments, and right-side whitespace.
# This is not a very smart process.
# It removes the last # in a line and everything after it.
# If a text # is in the line, put a comment # at the end of the line.
# DO NOT use this if you have blocks of text where blank lines are significant.
# DO NOT use this if you have long text with # in it.

smash = True
#smash = False

# just smash, don't load
smash_only = False

# leave smashed copy of file
smash_keep = True

# Once you set the above variables, save and run this file.
# Make sure that nothing else is using the serial port.
# Watch the screen. You'll be able to see everything it does.

# Of course, you could import this, instantiate the uploader class,
# set the variables, and then run uploader().upload(). If you want.

# ----------------------------------------------------------------------------------

# imports

import os,sys,time,serial

# self run

def run():

    uploader().upload()
    input('Press ENTER to close.')

# main class

class uploader:

    # fixed values
    baudrate = 115200
    timeout = 0.1
    fileblocksize = 1024
    rbuffer = ''

    def __init__(self):

        # port
        self.port = port
        if not self.port:
            self.port = '/dev/ttyUSB0'

        # local file system dir
        self.file_system_dir = file_system_dir
        if not self.file_system_dir:
            self.file_system_dir = os.getcwd()

        # excludes
        self.excludes = excludes
        if not self.excludes:
            self.excludes = []
        elif type(self.excludes) == str:
            self.excludes = excludes.split()
        self.excludes = set([os.path.basename(x) for x in self.excludes])

        # includes
        self.includes = includes
        if not self.includes:
            self.includes = []
        elif type(self.includes) == str:
            self.includes = includes.split()
        self.includes = set([os.path.basename(x) for x in self.includes])

        # notify
        print()
        print('REPL-Ace Uploader - Copyright (c) 2017 Clayton Darwin')
        print('ClaytonDarwin.com - claytondarwin@gmail.com')
        print('Port: {} Speed: {} Timeout: {}'.format(self.port,self.baudrate,self.timeout))
        print('System Root: {}'.format(self.file_system_dir))
        print('Exclude: {}'.format(list(self.excludes)))
        print('Include: {}'.format(list(self.includes)))
        print()

    def upload(self):

        # end message
        print('STARTING UPLOAD...')

        # create connection
        if not smash_only:
            self.connection = serial.Serial(port=self.port,baudrate=self.baudrate,timeout=self.timeout)
            self.connection.flush()
            self.connection.write([3,3]) # clear = ctrl-c
            #self.connection.write([4]) # soft reboot = ctrl-d
            self.recv(done=True) # full read

            # imports
            self.send('import os')

        # iterate through file system        
        for root,dirs,files in os.walk(self.file_system_dir):

            # drop bad dirs
            for x in dirs[:]:
                if x in self.excludes:
                    dirs.remove(x)
                elif includes and x not in includes:
                    dirs.remove(x)

            # drop bad files
            for x in files[:]:
                if x in self.excludes:
                    files.remove(x)
                elif includes and x not in includes:
                    files.remove(x)

            # sort
            dirs.sort()
            files.sort()

            # files in dirs already created
            for file in files:

                # make a temp file
                path1 = os.path.join(root,file)
                infile = open(path1)
                path2 ='smash_'+file
                outfile = open(path2,mode='w')
                for line in infile:
                    if not smash:
                        outfile.write(line)
                    else:
                        line2 = line.strip()
                        if (not line2) or line2.startswith('#'):
                            pass
                        elif '#' in line2:
                            outfile.write(line.rsplit('#',1)[0]+'\n')
                        else:
                            outfile.write(line)
                outfile.close()
                infile.close()

                # send temp file
                if not smash_only:
                    path3 = path1.replace(self.file_system_dir,'').lstrip('/')
                    self.send("outfile=open('{}',mode='wb')".format(path3))
                    infile = open(path2,mode='rb')
                    while 1:
                        data = infile.read(self.fileblocksize)
                        if not data:
                            break
                        self.send("outfile.write({})".format(data))
                    self.send("outfile.close()")

                # remove temp file
                if not (smash_only or smash_keep):
                    os.remove(path2)

            # dirs that need creating
            if not smash_only:
                for d in dirs:
                    path1 = os.path.join(root,d)
                    path2 = path1.replace(self.file_system_dir,'').lstrip('/')
                    dirname,basename = os.path.split(path2)
                    if dirname:
                        self.send("if '{1}' not in os.listdir('{0}'): os.mkdir('{0}/{1}')".format(dirname,basename))
                    else:
                        self.send("if '{0}' not in os.listdir(): os.mkdir('{0}')".format(basename))
                    self.send()
                    
                    self.send("print('LIST:','{0}',os.listdir('{0}'))".format(dirname))

        # close connection
        if not smash_only:
            self.connection.write([3,3]) # clear
            self.recv(done=True) # full read
            self.connection.close()

        # end message
        print('UPLOAD COMPLETE!')

    def send(self,line=''):

        self.connection.write([ord(x) for x in line+'\r'])
        self.recv()       

    def recv(self,done=False):

        # collect return from serial
        while 1:
            data = self.connection.read(1024)
            if not data:
                break
            else:
                self.rbuffer += data.decode(encoding='utf-8',errors='?')
        self.rbuffer = self.rbuffer.replace('\r','')

        # print return lines
        while '\n' in self.rbuffer:
            i = self.rbuffer.index('\n')
            line = self.rbuffer[:i]
            self.rbuffer = self.rbuffer[i+1:]
            print(line)

        # done
        if done:
            print(self.rbuffer)

if __name__ == '__main__':
    run()
