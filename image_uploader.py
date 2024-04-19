import time

from sqlalchemy import insert

from data import db_session
from data.uploads import Uploads


def upload_image(files):
    if 'file' not in files or files['file'].filename == '':
        exit()

    # Generate a new filename
    temp = files['file'].filename.split('.')
    new_filename = f"{time.time():.0f}.{temp[-1]}"
    destination_file_path = f'./img-uploads/{new_filename}'

    # Move the uploaded file to the destination
    if not files['file'].save(destination_file_path):
        print("WRONG!")
    else:
        print(destination_file_path)
        db_sess = db_session.create_session()
        image = insert(Uploads.file).values(destination_file_path)
        db_sess.add(image)
        db_sess.commit()
