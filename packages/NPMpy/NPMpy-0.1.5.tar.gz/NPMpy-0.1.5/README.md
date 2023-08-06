# Python code for curating Neurophotometrics data

This code was written to curate [Neurophotometrics (NPM)](https://neurophotometrics.com/) data for analysis in [pMat](https://github.com/djamesbarker/pMAT). In short, the NPM data is saved into two files: one containing the 415 control signals for every region recorded and the other the 470 gcamp signals for all regions recorded. However, pMat (currently) requires the opposite: one .csv files for each region that contains both the 415 and 470 signal. This requires quite a lot of copy and pasting which is tedious and prone to errors. This code was developed to automate this process.

## How to use this code?

A specific file structure is necessary for using the NPM python module for curating Neurophotometric data. The below example is a minimum necessary structure for the code to work. In short, you must input a directory that contains subdirectoriesfor each subject that contain the raw NPM data files (which also need to be renamed to .NPM.csv in order to be detected).

```
Data/      <---- This is the directory (path) that should be input to the curate_NPM() function. 
|-- Rat1/
|   |-- Rat1_415_data.npm.csv
|   |-- Rat1_470_data.npm.csv
|-- Rat2/
|   |-- Rat2_415_data.npm.csv
|   |-- Rat2_470_data.npm.csv
| ...
|-- RatN/
|   |-- RatN_415_data.npm.csv
|   |-- RatN_470_data.npm.csv
```


For a more general project file tree, I highly recommend something like the following to keep all of the experimental days and freezing data organized.

```
Data/
|-- Day1/          <---- This is the directory (path) that should be input to the "curated_NPM()" function. 
|   | -- Rat1/
|   |   |-- Rat1_415_data.npm.csv
|   |   |-- Rat1_470_data.npm.csv
|   |   |-- Freezing data/
|   |   |   |-- freezing_files       <---- Notice that freezing files are kept in their own folder
|
|-- Day2/           <---- This is the directory (path) that should be input to the "curated_NPM()" function. 
|   | -- Rat1/
|   |   |-- Rat1_415_data.npm.csv
|   |   |-- Rat1_470_data.npm.csv
|   |   |-- Freezing data/
|   |   |   |-- freezing_files
```

### General work flow

1. Organize the data into the above file structure
2. Rename all NPM data to have ".NPM.csv" at the end
3. Open your desired IDE (jupyter, spyder, etc)
4. Import this module 
    
    ``` import NPMpy as NPM```
    
5. Run curate_NPM(path_to_your_data)
6. Done!