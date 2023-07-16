# write-exif-google-photos
Write datetime, GPS and description metadata to Google Photos Takeout

This script will write EXIF metadata to images exported by Google Photos Takeout. It will write the datetime, GPS and description metadata coming from `json` files provided by Takeout. It writes the metadata to a copy of the original image, so the original image is not modified. The new image will be saved with the datetime in the filename.

- Note: EXIF metadata cannot be written to `avi`, `wmv`, `mkv`, `jfif` and `bmp` files. The script will skip these files. `avi`, `wmv` and `mkv` to `mp4`, and `jfif` and `bmp` to `jpg` conversion is recommended.
    - Some websites I used for conversion:
        - [avitomp4.net](https://avitomp4.net)
        - [cloudconvert.com/wmv-to-mp4](https://cloudconvert.com/wmv-to-mp4)
        - [cloudconvert.com/mkv-to-mp4](https://cloudconvert.com/mkv-to-mp4)
        - [cloudconvert.com/jfif-to-jpg](https://cloudconvert.com/jfif-to-jpg)
    - If you have `ffmpeg` installed, mkv to mp4 conversion can be done by: `ffmpeg -i <filename>.mkv -codec copy <filename>.mp4`

I have written this script to export my images from Google Photos without losing important metadata, especially datetime. Even though many images are exported with the correct datetime, some images are exported with the datetime of the export. I assume this happens to the images that have conflicting names.

## Usage

1. Download your Google Photos data from [Google Takeout](https://takeout.google.com/settings/takeout).
    - The script is written so that the directories are named as follows: `Takeout/Google Photos/Photos from <date>`. You need to give the script the path to the `Takeout` directory.
2. `python3 write.py -i <input_dir> -o <output_dir>`

## Requirements

- This script uses `ExifTool` to write metadata in images / videos. Make sure it's installed, found [here](https://exiftool.org).
