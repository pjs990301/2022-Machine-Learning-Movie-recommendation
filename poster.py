import pandas as pd
import requests
import time
import re



def download_poster(downloaded_image_dir, title, label, poster_path):

    imgUrl = 'http://image.tmdb.org/t/p/w185/' + poster_path

    local_filename = re.sub(r'\W+', ' ', title).lower().strip().replace(" ", "-") + '.jpg'

    try:
        session = requests.Session()
        r = session.get(imgUrl, stream=True, verify=False)
        with open(downloaded_image_dir + '/' + local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
    except:
        print('PROBLEM downloading', title, label, poster_path, imgUrl)

    time.sleep(1)


meta = pd.read_csv(
    'C:\\Users\\HOME\\Documents\\GitHub\\2022-Machine-Learning-Movie-recommendation\\data\\movies_metadata_temp.csv')
meta = meta[['id', 'title', 'poster_path']]
meta = meta.dropna()
print(meta)
# download image by iterate pandas


for index, row in meta.iterrows():
    download_poster(
        'images_movies_id',
        str(row['id']),
        str(row['title']),
        row['poster_path']
    )
