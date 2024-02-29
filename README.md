# Hugo2Ghost
A python script helps migrating your hugo post to ghost with support of to add your old post tags and post feature images. 

**Supports**
1) Adds hugo tags to ghost
2) Hugo subtitle to Meta Description in Ghost
3) Preserve Dates
4) Adds Feature Images


## Usage
```
Python3 hugo_to_ghost.py input_dir output.json
```
Outputs a "output.json" file and a "images" directory which is having all the feature images.

### Importing the data to Ghost
After you have generated the file, go to your ghost admin setting, Advanced->Import/Export->Universal Import and choose your generated .json file.
After that, copy the entire images folder to your Ghost installation path /content/

## To do
- [ ] Add Image resize support for feature Images.
- [ ] Add support to remove more custom shortcodes.
- [ ] Add support to migrate all images.
- [ ] Add Test Cases.