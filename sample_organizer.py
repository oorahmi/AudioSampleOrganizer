#!/usr/bin/python

'''
OORAHMI

Organize your samples from splice or wherever you dump them, 
since the amount of directories you have to open to get to samples 
is ridiculous and makes me not listen to any samples.
Useful if you're downloading from splice or somewhere and don't care what the pack names are anymore

To change how your files are organized modify the global list: sample_directories
each entry in this list corresponds

sample_organizer stat <sample_directory_1>  <sample_directory_2> ...
 - get a listing of common strings that occur for your sample library 

sample_organizer copy_samples <source_directory> <destination_directory> 
 - take samples from source and copy them in destination based on your sample_directories list 
 - destination is the top level directory of where you're putting all your samples
    ie. destination/snare, destination/hat, ... and so on

sample_organizer move_samples <source_directory> <destination_directory> 
 - little more dangerous
 - take samples from source and move them in destination based on your sample_directories list 
 - destination is the top level directory of where you're putting all your samples
    ie. destination/snare, destination/hat, ... and so on

sample_organizer reorganize <organized_sample_directory> <new_directory_name> 
 - Used if you have a new directory and want to check all samples to see if they match that name and reorganize.
   ie. made a new dir called 'tamborine' so find all my organized samples that have 'tamborine' and put them in new dir.
 - doesn't take capital letters seriously, i guess just like your os.
'''
from operator import itemgetter
import re
import shutil
from collections import OrderedDict
import os 
import errno
import sys
import pprint

# want to skip errant files like .asd, .ds_store
allowed_file_extensions = {'.mp3', '.wav', '.aif'}

def main(args):

    # gather all organizational data
    sample_directories = []
    with open(os.path.join(os.getcwd(), 'sample_directory_list.txt'),'r') as sample_directory_list_file:
        for line in sample_directory_list_file.readlines():
            sample_directories.append(line.rstrip())

    strings_dict = {}
    string_filenames = []
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'strings')):
        for name in files:
            string_filenames.append(os.path.join(root, name))

    for filename in string_filenames:
        with open(filename, 'r') as strings_file:
            string_type = os.path.splitext(os.path.basename(strings_file.name))[0]
            if string_type not in sample_directories:
                print('Error: ', filename, ' not found to match a directory in sample_directory_list.txt')
                continue
            strings_dict[string_type] = []
            for line in strings_file.readlines():
                strings_dict[string_type].append(line.rstrip())

    def recursiveSearch(path):
        #TODO: maybe skip a favorites directory?
        # prob not since this whole script is meant to just begin to organize your sample library
        # from which then you should customize on your own. This organization is a good buffer to browsing.
        for root, dirs, files in os.walk(path):
            for name in files:
                sample_filename = os.path.join(root, name)
                file_extension = os.path.splitext(os.path.basename(sample_filename))[1]  

                if file_extension in allowed_file_extensions:
                    sample_filenames.append(sample_filename)

    def matchAndProcessSamples(destination, move_files):
        # create all destination directories, if they don't exist
        for sample_directory in sample_directories:
            sample_parent_dir = os.path.join(destination, sample_directory)
            try:
                os.makedirs(sample_parent_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            #NOTE: failed on windows 10, uhhh
            #os.makedirs(os.path.dirname(sample_parent_dir), exist_ok=True)

        for sample_filename in sample_filenames:
            lowered_sample_endname = os.path.splitext(os.path.basename(sample_filename))[0].lower()
            sample_dir_index = 0
            sample_directory = ''
            matched = False
            while(sample_dir_index < len(sample_directories) and not matched):
                sample_directory = sample_directories[sample_dir_index]

                # check that the sample name contains
                # NOTE: slow performance here
                
                if sample_directory in lowered_sample_endname:
                    matched = True
                elif sample_directory in strings_dict:
                    for matcher_string in strings_dict[sample_directory]:
                        if matcher_string in lowered_sample_endname:
                            matched = True
                            break

                sample_dir_index += 1
            
            just_end_filename = os.path.basename(sample_filename)
            end_file_destination = ''

            if move_files:
                # no match?
                if sample_dir_index == len(sample_directories):
                    end_file_destination = os.path.join(destination, 'unknown', just_end_filename)
                else:
                    end_file_destination = os.path.join(destination, sample_directory, just_end_filename)
                if not os.path.exists(end_file_destination):
                    # move file
                    os.rename(sample_filename, end_file_destination)
            else:
                # no match?
                if sample_dir_index == len(sample_directories):
                    end_file_destination = os.path.join(destination, 'unknown', just_end_filename)
                else:
                    end_file_destination = os.path.join(destination, sample_directory, just_end_filename)
                if not os.path.exists(end_file_destination):
                    shutil.copy(sample_filename, end_file_destination) 


    sample_filenames = []

    if args[0] == 'stat':
        '''
        Idea is to print a list a strings and their occurency count
        to pick smart names for folders, ie. snare showed up a lot, 
        make a snare dir and throw them there.
        '''
        for directory in args[1:]:
            recursiveSearch(directory)
        #sample_filenames = ['ThisIsATest_haha_yeah_a_b', 'NumberTwo','haha_haha_Haha_three', 'so-snare-boy-high', 'kick this kid']

        #TODO: think about organizing or statting by parent directory name of samples

        strings_frequency_dict = OrderedDict() # interesting strings! 

        # based on name
        for sample_name in sample_filenames:
            # get end without extension
            sample_name = os.path.splitext(os.path.basename(sample_name))[0]

            # try splits
            scored_split_parts = sample_name.split('_')
            dash_split_parts = sample_name.split('-')
            space_split_parts = sample_name.split(' ')

            # camel case regex
            camel_case_parts = re.sub('(?!^)([A-Z][a-z]+)', r' \1', sample_name).split()

            # who split the best?
            best_splits = []

            for splitter in [scored_split_parts, dash_split_parts, space_split_parts, camel_case_parts]:
                if len(splitter) > len(best_splits):
                    best_splits = splitter
                
            # gather string frequencies
            for string in best_splits:
                string = string.lower()
                if string in strings_frequency_dict:
                    strings_frequency_dict[string] += 1
                else:
                    strings_frequency_dict[string] = 1

        pprint.pprint(sorted(strings_frequency_dict.items(), key=itemgetter(1)))
    
    # move sample files to directories based on directory names
    elif args[0] == 'organize_samples_copy':
        source = args[1]
        destination = args[2]
        recursiveSearch(source)
        matchAndProcessSamples(destination, False)

    elif args[0] == 'organized_samples_move':
        #TODO: pretty scary, add warning
        source = args[1]
        destination = args[2]
        recursiveSearch(source)
        matchAndProcessSamples(destination, True)


    # Used if you have a new directory and want to check all samples to see if they match that name and reorganize.
    # ie. made a new dir called 'tamborine' so find all my organized samples that have 'tamborine' and put them in new dir.
    elif args[0] == 'reorganize':
        organized_sample_directory = args[1]
        organize_string = args[2].lower()
        #TODO: add to sample_directory_list.txt ?
        # make new dir
        try:
            os.makedirs(os.path.join(organized_sample_directory, organize_string))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        recursiveSearch(organized_sample_directory)

        for sample_filename in sample_filenames:
            just_end_filename = os.path.basename(sample_filename)
            if organize_string in sample_filename.lower():
                # move file
                os.rename(sample_filename, os.path.join(organized_sample_directory, organize_string, just_end_filename))




if __name__ == "__main__":
    main(sys.argv[1:])