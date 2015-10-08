"""
Author: Maksim Korolev
Tests for function_code
"""

import unittest, tempfile, shutil, os, re
from function_code import function
import random, uuid
import exrex #this creates a string from a regex, useful for creating test files

class MyTest(unittest.TestCase):

    #assert no matches are made if keyword doesn't match
    def test_strange_keyword_input(self):
        test_output, function_output = create_test_files()
        no_output_test = test_output[1]
        no_output_function = function_output[1]
        self.assertEqual(no_output_test, no_output_function)

    #assert exception is raised if file path doesn't exist
    def test_strange_path_input(self):
        self.assertRaises(OSError, function, 'jlfajdljfdls', 'new')

    #manually create test files with spaces, random exensions, and random folder placement
    def test_normal_input(self):
        test_output, function_output = create_test_files()
        self.assertEqual(test_output[0], function_output[0])       

    #test function output to large set of randomly generated files and folders
    def test_large_set(self):
        test_output, function_output = create_large_set_test_files()
        self.assertEqual(test_output,function_output)

#manually create test files
def create_test_files():
    newdir = tempfile.mkdtemp()
    newfile = open(os.path.join(newdir, 'newtext.txt'), 'a')
    newfile.close()
    newfile = open(os.path.join(newdir, 'text file'), 'a')
    newfile.close()
    newfile = open(os.path.join(newdir, 'videonew.avi'), 'a')
    newfile.close()

    newdirpath1 = os.path.join(newdir, "newtext") 
    os.makedirs(newdirpath1)
    newfile = open(os.path.join(newdirpath1, 'newtext2.txt'), 'a')
    newfile.close()
    newfile = open(os.path.join(newdirpath1, 'textfile2'), 'a')
    newfile.close()
    newfile = open(os.path.join(newdirpath1, 'video new2.avi'), 'a')
    newfile.close()

    newdirpath2 = os.path.join(newdirpath1, "new text2") 
    os.makedirs(newdirpath2)
    newfile = open(os.path.join(newdirpath2, 'video new2.avi'), 'a')
    newfile.close()


    newdirpath3 = os.path.join(newdirpath2, "new text2") 
    os.makedirs(newdirpath3)

    function_output = function(newdir, 'new'),function(newdir, 'fafodejoaehjojfoija')

    shutil.rmtree(newdir)

    return (sorted([newdir+":"+"2", newdirpath1+":"+"2", newdirpath2+":"+"1",newdirpath3+":"+"0"]),
    sorted([newdir+":"+"0", newdirpath1+":"+"0", newdirpath2+":"+"0",newdirpath3+":"+"0"])),(function_output)

#generate large set of random sets of files and folders to test
def create_large_set_test_files():
    originaldir = tempfile.mkdtemp()
    newdir = originaldir
    filecount = []
    count = 0

    file_extensions = ['.txt', '.jpg', '.txt', '.exe', '.avi', '.bat']
    random_extension = file_extensions[int(round(random.random()*5.49))]

    searchstring = '^[a-zA-Z]+_TESTResult\w*'
    endrange = 100

    #endrange instances of folder or file creation
    for i in range(endrange):
        if i == endrange-1:
            filecount.append(newdir+":"+str(count))
        #either:
        elif random.random() > .3:
            #create new file in current dir with regex
            if random.random() > .5:
                filename = exrex.getone(searchstring) + random_extension
                newfile = open("\\\\?\\" +os.path.join(newdir, filename), 'w+')
                newfile.close()
                count+=1
            #or create new file without regex
            else:
                filename = str(uuid.uuid4())+ random_extension
                newfile = open("\\\\?\\" +os.path.join(newdir, filename), 'w+')
                newfile.close()
                if re.search(searchstring, filename) != None:
                    count+=1
        #or create new subdirectory
        else:
            filecount.append(newdir+":"+str(count))
            newdir = os.path.join(newdir, str(i))
            os.mkdir("\\\\?\\" + newdir)
            count = 0

    function_output = function(originaldir, '^[a-zA-Z]+_TESTResult.*')
    shutil.rmtree(originaldir)

    return sorted(filecount), function_output

if __name__ == "__main__":
    unittest.main()