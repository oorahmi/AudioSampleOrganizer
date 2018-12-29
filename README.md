# AudioSampleOrganizer
* Moves samples based on their names to corresponding folders you can define
* Print out strings and their frequency from your sample filenames

Useful if you're downloading from splice or somewhere and don't care what the pack names are anymore and just want to flatten the hierarchy.

The amount of directories you have to open to get to samples is ridiculous and makes me not listen to any samples.

## Organization
### Sample Directories
All samples are put into a directory depending on the names listed in `sample_directory_list.txt`
Each name is also used to compare directly against a sample filename to see which directory it should go.
* ie. All files with 'snare' in them with go into the 'snare' directory.
```
    snare1.wav 
    fat_snare.wav 
    GoToSnare.wav               ----all placed--->      'YourSamplePath/snare' directory`
    badly-named-snare.wav 
    my snare.wav  

```

I am only detecting if a string is in a filename (string contains) for this python app. Nothing fancy.

The order of names in `sample_directory_list.txt` may matter if you have some badly named files.
`hihat_snare.wav` would go into `snare` based on the current order.

### Use multiple strings
Sample folders can also match against several strings if you define a new file in the `strings` directory
Files in the `strings` directory correspond to folders defined by `sample_directory_list.txt`
These text files increase the amount of strings to compare against to add to a sample directory.
ie. `percussion.txt` contains `shaker`, `clave`, and `block`
`shaker.wav clave.wav block.wav` now all go into the `percussion` folder.

## Example Modification
## Adding a new directory for samples with multiple strings
**uhh maybe write cli for this**
- Pick a good name that will map uniquely to some sample filenames, for example let's try `animal`
- Add the name (`animal`) to `sample_directory_list.txt`
- Add a file called `animal.txt` into the `strings` directory
- Add some more good strings into `animal.txt` that may match animals like `dog` `bark` `roar` `meow`
    - Now filenames like `animal.wav dog_barking.wav LionRoar.wav cat-meow.wav` will all be ready to go into a folder called `animal`
- Use the python app on the command line to move or copy the files to your organization following this new setup.



### Install
* *Requirements*
    * Python 3+ (I wrote this with python 3.7) 

Clone this repository somewhere on your machine, preferably near your samples 
`git clone https://github.com/oorahmi/AudioSampleOrganizer.git`

# Command Line Usage 


### Copy Samples
```
sample_organizer.py copy_samples source_directory destination_directory
```
 - Take samples from source and copy them in destination based on your sample_directories list 
 - Destination is the top level directory of where you're putting all your samples
    ie. destination/snare, destination/hat, ... and so on

### Move Samples
```
sample_organizer.py move_samples source_directory destination_directory
```
 - little more dangerous
 - take samples from source and move them in destination based on your sample_directories list 
 - destination is the top level directory of where you're putting all your samples
    ie. destination/snare, destination/hat, ... and so on
 - Useful if you've just changed your organization in some way just do: 
    `sample_organizer move_samples <source_directory> <source_directory>`
    and you can reorganize all your samples in place!

### Reorganize Samples
```
sample_organizer.py reorganize organized_sample_directory new_directory_name
```
 - ...thinking about this...
 - partial reorganize
 - Used if you have a new directory and want to check all samples to see if they match that name and reorganize.
   ie. make a new dir called 'tamborine' so find all my organized samples that have 'tamborine' and put them in new dir.
 - doesn't take capital letters seriously, i guess just like your os.

### Samples Statistics
```
sample_organizer stat sample_directory_1  sample_directory_2 ... sample_directory_n
```
 - get a listing of common strings that occur for your sample library 
 - useful to see how you may want to organize your sample library and edit folder names in `sample_directory_list` or files in `strings`

