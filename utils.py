from os import path
from random import randint
from json import loads, load
import glob
from json import dumps
import requests
import leancloud
from credentials import BOT_TOKEN, LEAN_APP_ID, LEAN_APP_KEY

leancloud.init(LEAN_APP_ID, LEAN_APP_KEY)

STORAGE = "meta-shota/img/shota/"
TG_API_FILE = "https://api.telegram.org/bot{}/getFile?file_id=".format(
    BOT_TOKEN)
TG_API_DL = "https://api.telegram.org/file/bot{}/".format(BOT_TOKEN)


def valid(pic):
    return len(pic.get("file_id")) > 50


def get_picture():
    Picture = leancloud.Object.extend('Picture')
    query = Picture.query
    query.skip(randint(0, query.count()))
    return query.first()


def dl_picture(pic):
    file = "{}/{}.jpg".format(STORAGE, pic.id)
    if path.isfile(file):
        return pic
    file_id = pic.get("file_id")
    file_path = loads(requests.get(
        TG_API_FILE + file_id).content)["result"]["file_path"]
    res = requests.get(TG_API_DL + file_path)
    with open(file, 'wb') as f:
        f.write(res.content)
        f.close()
    return pic


def parse_caption(txt):
    stage_1 = txt.split('*')
    title = stage_1[1].strip()
    stage_2 = stage_1[2].split('#')
    author = stage_2[0].split(':')[1].strip()
    stage_3 = '#'.join(stage_2[1:]).split(' ')
    tags = list(map(lambda x: x.replace('#', '').strip(), stage_3[0:-1]))
    url = stage_3[-1].strip()
    if url[0:4] != 'http':
        url = 'https://' + url
    return {
        'title': title,
        'author': author,
        'tags': tags,
        'url': url
    }


def random_shota(num=9):
    all = glob.glob("meta-shota/data/*.json")
    length = len(all)
    pic_ids = set()
    pics = []
    while len(pic_ids) < num:
        pic_id = randint(0, length) % length
        pic_ids.add(pic_id)
    pic_ids = list(pic_ids)
    for i in range(num):
        pic = load(open(all[pic_ids[i]], 'r'))
        pics.append(pic)
    return pics


def latest_shota(num=9):
    all = glob.glob("meta-shota/data/*.json")
    latest = sorted(all, key=path.getctime, reverse=True)
    pics = []
    for i in range(num):
        pic = load(open(latest[i], 'r'))
        pics.append(pic)
    return pics


if __name__ == "__main__":
    Picture = leancloud.Object.extend('Picture')
    query = Picture.query
    query.skip(900)
    ob_list = query.find()
    for pic in ob_list:
        data_file = "meta-shota/data/{}.json".format(pic.id)
        if valid(pic):
            dl_picture(pic)
        else:
            continue
        if not path.isfile(data_file):
            caption = pic.get('caption')
            print('Processing {}'.format(pic.id))
            if caption:
                info = parse_caption(caption)
                info['id'] = pic.id
                with open(data_file, 'w') as f:
                    f.write(dumps(info, ensure_ascii=False))
                    f.close()
            else:
                continue
