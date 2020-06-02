import datetime
import logging
import os
import shutil
import uuid

from django.core.files.storage import default_storage

from api.models import Document
from api.utils import check_run


def setup_environment():
    scan_dir = os.path.join(default_storage.base_location, 'scan')
    raw_dir = os.path.join(scan_dir, 'raw')
    ocr_dir = os.path.join(scan_dir, 'ocr')
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)
    if not os.path.exists(ocr_dir):
        os.makedirs(ocr_dir)

    return scan_dir, raw_dir, ocr_dir


def drop_temporaries(scan_dir):
    shutil.rmtree(scan_dir, ignore_errors=True)


def scan_image(target_dir):
    logging.debug('Scanning images')
    return check_run([
        'scanimage',
        '--format', 'tiff',
        '--resolution', '300',
        '--source', 'ADF Duplex',
        f'--batch={target_dir}/raw%02d.tiff',
        '--batch-print',
        '--page-width', '210', '--page-height', '297',
        '--ald=yes',
        '-d', 'fujitsu:ScanSnap iX500:1201996',
    ]).decode('utf-8').strip().split('\n')


def filter_empty_pages(images):
    logging.debug('Detecting empty pages')
    for image in images:
        result = check_run([
            'convert', image,
            '-virtual-pixel', 'White',
            '-blur', '0x15',
            '-fuzz', '15%',
            '-trim', 'info:']).decode('utf-8').strip()
        w, h = map(int, result.split(' ')[2].split('x'))
        if w < 50 or h < 50:
            logging.debug(f'Empty page `{image}` detected')
            os.unlink(image)
            continue
        yield image


def create_multi_page_tiff(images, target_dir):
    logging.debug('Creating multi-page TIFF')
    outfile = os.path.join(target_dir, 'raw.tiff')
    check_run(['convert'] + images + [outfile])
    return outfile


def store_document(path):
    shutil.move(path, default_storage.base_location)
    path = os.path.basename(path)
    uploaded = datetime.datetime.now(tz=datetime.timezone.utc)
    return Document.create(uploaded=uploaded, path=path, name=path)


def ocr(infile, outfile):
    logging.debug(f'OCR on {infile}')
    check_run(
        ['tesseract', infile, outfile, '-l', 'deu+eng', 'pdf']
    )
    shutil.move(outfile + '.pdf', outfile)
    return outfile


def create_multipage_tiff(images, raw_dir):
    if len(images) == 1:
        multi_page = images[0]
    else:
        multi_page = create_multi_page_tiff(images, raw_dir)
    return multi_page


def scan():
    scan_dir, raw_dir, ocr_dir = setup_environment()
    try:
        images = scan_image(raw_dir)
        images = list(filter_empty_pages(images))
        images = create_multipage_tiff(images, raw_dir)

        path = ocr(images, os.path.join(ocr_dir, str(uuid.uuid4())))

        doc = store_document(path)
        logging.debug('Predicting category')
        doc.predict()
        logging.info(f'Predicted document category is {doc.category.name}')
        doc.index()
        doc.save()
        logging.info(f'{doc} imported')
        return doc
    finally:
        drop_temporaries(scan_dir)
