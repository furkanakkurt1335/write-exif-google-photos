import os, re, random, argparse, subprocess, logging, json
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='write.log')

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-dir', type=str, help='Directory to read from', required=True)
parser.add_argument('-o', '--output-dir', type=str, help='Directory to write to', required=True)
args = parser.parse_args()

im_dir = args.input_dir
edited_im_dir = args.output_dir
im_json_match_d = {}
multiple_pattern = '\(\d+?\)$'
im_s = set()
json_s = set()
for root, dirs, files in os.walk(im_dir):
    im_l = [f for f in files if not f.endswith('.json') and f != '.DS_Store']
    for im in im_l:
        im_s.add(os.path.join(root, im))
    json_l = [f for f in files if os.path.splitext(f)[1] == '.json' and f != 'metadata.json']
    for json_t in json_l:
        json_s.add(os.path.join(root, json_t))
        with open(os.path.join(root, json_t), 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        title = json_data['title'].replace("'", '_').replace(';', '_')
        title_base, title_ext = os.path.splitext(title)
        image_in_title = title_base[:51-len(title_ext)] + title_ext
        json_base, json_ext = os.path.splitext(json_t)
        multiple_search = re.search(multiple_pattern, json_base)
        if multiple_search:
            multiple_text = multiple_search.group()
            image_in_title_base, image_in_title_ext = os.path.splitext(image_in_title)
            new_image_in_title = image_in_title_base + multiple_text + image_in_title_ext
            if os.path.exists(os.path.join(root, new_image_in_title)):
                im_json_match_d[os.path.join(root, new_image_in_title)] = os.path.join(root, json_t)
            elif os.path.exists(os.path.join(root, image_in_title)):
                im_json_match_d[os.path.join(root, image_in_title)] = os.path.join(root, json_t)
            else:
                print('No image for json: {}'.format(os.path.join(root, json_t)))
        elif os.path.exists(os.path.join(root, image_in_title)):
            im_json_match_d[os.path.join(root, image_in_title)] = os.path.join(root, json_t)
        else:
            print('No image for json: {}'.format(os.path.join(root, json_t)))
            print('Image in title: {}'.format(image_in_title))
            print('-' * 50)
im_match_l, json_match_l = im_json_match_d.keys(), im_json_match_d.values()
for im in im_s:
    if im not in im_match_l:
        print('No json for image: {}'.format(im))
        im_title = os.path.basename(im)
        im_title_base, im_title_ext = os.path.splitext(im_title)
        new_im_title = im_title
        while os.path.exists(os.path.join(edited_im_dir, new_im_title)):
            new_im_title = im_title_base + '-' + str(random.randint(1000, 9999)) + im_title_ext
        new_im = os.path.join(edited_im_dir, new_im_title)
        call = 'cp -v "{}" "{}"'.format(im, new_im)
        logging.info('Running `{}`'.format(call))
        process = subprocess.run(call, shell=True, capture_output=True)
        stdout, stderr = process.stdout.decode('utf-8').strip(), process.stderr.decode('utf-8').strip()
        if stdout:
            logging.info(stdout)
        if stderr:
            logging.error(stderr)
for json_t in json_s:
    if json_t not in json_match_l:
        print('No image for json: {}'.format(json_t))

if not os.path.exists(edited_im_dir):
    os.mkdir(edited_im_dir)
for k, v in im_json_match_d.items():
    if not os.path.exists(k):
        print('Image does not exist: {}'.format(k))
    # else:
    #     print('Image exists: {}'.format(k))
    if not os.path.exists(v):
        print('JSON does not exist: {}'.format(v))
    # else:
    #     print('JSON exists: {}'.format(v))
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
    description = json_data['description'].strip().replace('\n', ' ; ').replace('"', "'")
    if description:
        md_l.append('-Caption-Abstract="{}" -Description="{}" -ImageDescription="{}"'.format(description, description, description))
    new_im = str(time.strftime('%Y%m%d_%H%M%S') + os.path.splitext(k)[1]).lower()
    new_im_path = os.path.join(edited_im_dir, new_im)
    while os.path.exists(new_im_path):
        new_im = str(time.strftime('%Y%m%d_%H%M%S') + '-' + str(random.randint(1000, 9999)) + os.path.splitext(k)[1]).lower()
        new_im_path = os.path.join(edited_im_dir, new_im)
    outfile_str = '-o "{}"'.format(os.path.join(edited_im_dir, new_im))
    md_l.append(outfile_str)
    logging.info('Original image: {}'.format(k))
    k_lower = k.lower()
    if k_lower.endswith('.bmp') or k_lower.endswith('.avi') or k_lower.endswith('.wmv') or k_lower.endswith('.mkv'):
        call = 'cp -v "{}" "{}"'.format(k, new_im_path)
    else:
        call = 'exiftool "{}" {} -m'.format(k, ' '.join(md_l))
    logging.info('Running `{}`'.format(call))
    process = subprocess.run(call, shell=True, capture_output=True)
    stdout, stderr = process.stdout.decode('utf-8').strip(), process.stderr.decode('utf-8').strip()
    if stdout:
        logging.info(stdout)
    if stderr:
        logging.error(stderr)
        if 'looks more like a JPEG' in stderr:
            k_jpeg = os.path.splitext(k)[0] + '.jpg'
            new_im_path_jpeg = os.path.splitext(new_im_path)[0] + '.jpg'
            call = 'cp -v "{}" "{}"'.format(k, k_jpeg)
            logging.info('Running `{}`'.format(call))
            process = subprocess.run(call, shell=True, capture_output=True)
            stdout, stderr = process.stdout.decode('utf-8').strip(), process.stderr.decode('utf-8').strip()
            if stdout:
                logging.info(stdout)
            if stderr:
                logging.error(stderr)
            while os.path.exists(new_im_path_jpeg):
                new_im = str(time.strftime('%Y%m%d_%H%M%S') + '-' + str(random.randint(1000, 9999)) + os.path.splitext(new_im_path_jpeg)[1]).lower()
                new_im_path_jpeg = os.path.join(edited_im_dir, new_im)
            md_l[-1] = '-o "{}"'.format(new_im_path_jpeg)
            call = 'exiftool "{}" {} -m'.format(k_jpeg, ' '.join(md_l))
            logging.info('Running `{}`'.format(call))
            process = subprocess.run(call, shell=True, capture_output=True)
            stdout, stderr = process.stdout.decode('utf-8').strip(), process.stderr.decode('utf-8').strip()
            if stdout:
                logging.info(stdout)
            if stderr:
                logging.error(stderr)
    logging.info('New image: {}'.format(new_im_path))
