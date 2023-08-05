# PIM_VIDEO PYTHON PACKAGE LIBRARY MANUAL
## Description
This program will merge left and right videos which are recorded in ABI eye research group web experience recording folder. 

It will automatically determine the timestamps of left and right videos and merge into one single video called `left_right_combined.mp4` in which left and right vidoes are trimmed accordingly and combined synchronously.
## Installation requirements and guide
### Anaconda
To install this program, `Anaconda python distributing program` and `Anaconda Powershell Prompt` are needed.  
If you do not have `Anaconda`, please use the following links to download and install:  
Download link: https://www.anaconda.com/products/distribution  
Installation guide link: https://docs.anaconda.com/anaconda/install/  
### PIP install
To install `pim_video`, you have to use `Anaconda Powershell Prompt`.  
After that, you can use the `pim_video`` from any command prompt.  
In `Anaconda Powershell Prompt`:
```
pip install pim_video
```  
## Usage requirements and guide
### FFMPEG
To use `pim_video`, you must have `ffmpeg` in your computer which is essential program for our program process.  
If you do not have `ffmpeg`, please use one of the following links:  
For windows: https://www.wikihow.com/Install-FFmpeg-on-Windows  
For mac: https://bbc.github.io/bbcat-orchestration-docs/installation-mac-manual/  
### Example usage
```
pim_video -d (directory to pim recorded folder)
```
There is a example folder under `development` folder.  
If you want to test this program, you can clone this repository, install `pim_video` and run the following command:
```
pim_video -d development/example_folder
```
