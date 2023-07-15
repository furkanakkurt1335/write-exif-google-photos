import os, re
from datetime import datetime
import random

def get_ext(path):
    return os.path.splitext(path)[1]

home = os.path.expanduser("~")
im_dir = os.path.join(home, '2011-2015')
im_s = set()
json_s = set()
im_json_match_d = {}
multiple_pattern = '\(\d+\)$'
im_path_d = {}
json_path_d = {}
for root, dirs, files in os.walk(im_dir):
    im_l = [f for f in files if not f.endswith('.json') and f != '.DS_Store']
    json_l = [f for f in files if os.path.splitext(f)[1] == '.json' and f != 'metadata.json']
    for im in im_l:
        if im in im_s:
            print('Duplicate: {}'.format(os.path.join(root, im)))
        im_s.add(os.path.join(root, im[:46]))
        im_path = os.path.join(root, im)
        im_path_d[os.path.join(root, im[:46])] = im_path
    for json in json_l:
        json_base = os.path.splitext(json)[0]
        multiple_search = re.search(multiple_pattern, json_base)
        if multiple_search:
            multiple_text = multiple_search.group()
            im_json_wo_multiple = re.sub(multiple_pattern, '', json_base)
            im_json_split = os.path.splitext(im_json_wo_multiple)
            json_base = im_json_split[0] + multiple_text + im_json_split[1]
        if json_base in json_s:
            print('Duplicate: {}'.format(os.path.join(root, json)))
        json_s.add(os.path.join(root, json_base[:46]))
        json_path = os.path.join(root, json)
        json_path_d[os.path.join(root, json_base[:46])] = json_path
for im in im_s:
    if im not in json_s:
        print('Image without json: {}'.format(os.path.join(root, im)))
for k, v in im_path_d.items():
    if k not in json_path_d:
        print('Image without json: {}'.format(v))
    else:
        im_json_match_d[v] = json_path_d[k]
for json in json_s:
    if json not in im_s:
        print('JSON without image: {}'.format(os.path.join(root, json)))

edited_im_dir = os.path.join(home, '2011-2015 edited')
import json
if not os.path.exists(edited_im_dir):
    os.mkdir(edited_im_dir)
for k, v in im_json_match_d.items():
    if not os.path.exists(k):
        print('JSON does not exist: {}'.format(k))
    # else:
    #     print('JSON exists: {}'.format(k))
    if not os.path.exists(v):
        print('Image does not exist: {}'.format(v))
    # else:
    #     print('Image exists: {}'.format(v))
    md_l = []
    with open(v, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    if 'photoTakenTime' not in json_data:
        print('No photoTakenTime: {}'.format(v))
    timestamp = int(json_data['photoTakenTime']['timestamp'])
    time = datetime.fromtimestamp(timestamp)
    time_str = time.strftime('%Y:%m:%d %H:%M:%S')
    md_l.append('-DateTimeOriginal="{}" -CreateDate="{}"'.format(time_str, time_str))
    if 'geoData' not in json_data:
        print('No geoData: {}'.format(v))
    latitude = json_data['geoData']['latitude']
    if latitude:
        md_l.append('-GPSLatitude={} -GPSLatitudeRef=N'.format(latitude))
    longitude = json_data['geoData']['longitude']
    if longitude:
        md_l.append('-GPSLongitude={} -GPSLongitudeRef=E'.format(longitude))
    altitude = json_data['geoData']['altitude']
    if altitude:
        md_l.append('-GPSAltitude={} -GPSAltitudeRef="Above Sea Level"'.format(altitude))
    if 'description' not in json_data:
        print('No description: {}'.format(v))
    description = json_data['description'].strip()
    if description:
        md_l.append('-Caption-Abstract="{}" -Description="{}" -ImageDescription="{}"'.format(description, description, description))
    new_im = str(time.strftime('%Y%m%d_%H%M%S') + os.path.splitext(k)[1]).lower()
    new_im_path = os.path.join(edited_im_dir, new_im)
    while os.path.exists(new_im_path):
        new_im = str(time.strftime('%Y%m%d_%H%M%S') + '-' + str(random.randint(1000, 9999)) + os.path.splitext(k)[1]).lower()
        new_im_path = os.path.join(edited_im_dir, new_im)
    outfile_str = '-o "{}"'.format(os.path.join(edited_im_dir, new_im.lower()))
    md_l.append(outfile_str)
    if k.lower().endswith('.bmp') or k.lower().endswith('.avi') or k.lower().endswith('.wmv'):
        os.system('cp -v "{}" "{}" 2>&1'.format(k, new_im_path))
        os.system('echo copied "{}" to "{}" >> out.log'.format(k, new_im_path))
    else:
        os.system('exiftool "{}" {} >> out.log 2>&1'.format(k, ' '.join(md_l)))
        os.system('echo used exiftool "{}" {} >> out.log'.format(k, ' '.join(md_l)))
    os.system('echo >> out.log')
