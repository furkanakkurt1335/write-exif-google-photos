# write-exif-google-photos
Write datetime, GPS and description metadata to Google Photos Takeout

This script will write EXIF metadata to images exported by Google Photos Takeout. It will write the datetime, GPS and description metadata coming from `json` files provided by Takeout. It writes the metadata to a copy of the original image, so the original image is not modified. The new image will be saved with the datetime in the filename.

Note: EXIF metadata cannot be written to `AVI` and `BMP` files. The script will skip these files. `AVI` to `MP4` conversion is recommended.

I have written this script to export my images from Google Photos without losing important metadata, especially datetime. Even though many images are exported with the correct datetime, some images are exported with the datetime of the export. I assume this happens to the images that have conflicting names.