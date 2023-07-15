# write-exif-google-photos
Write datetime, GPS and description metadata to Google Photos Takeout

This script will write EXIF metadata to images exported by Google Photos Takeout. It will write the datetime, GPS and description metadata coming from `json` files provided by Takeout. It writes the metadata to a copy of the original image, so the original image is not modified. The new image will be saved with the datetime in the filename.

- Note: EXIF metadata cannot be written to `avi`, `wmv` and `bmp` files. The script will skip these files. `avi` and `wmv` to `mp4` conversion is recommended.
    - Some websites I used: https://avitomp4.net and https://cloudconvert.com/wmv-to-mp4 .

I have written this script to export my images from Google Photos without losing important metadata, especially datetime. Even though many images are exported with the correct datetime, some images are exported with the datetime of the export. I assume this happens to the images that have conflicting names.

## Requirements

This script uses `ExifTool` to write metadata in images / videos. Make sure it's installed, found [here](https://exiftool.org).

