from fastapi import FastAPI
import csv
import random
import datetime
import uuid
import base64
import os
import utils.image
import json
from pathlib import Path

DATASET = {}


def load_data():
    reader = csv.reader(open('names.csv', 'r'))
    for i, row in enumerate(reader):
        name, gender, _, _ = row
        DATASET[i] = {
            "name": name,
            "gender": gender,
        }


load_data()


class RandomPeople:
    id = ""
    name = ""
    gender = ""
    dob = ""
    photo = ""
    age = 0

    def __init__(self):
        self.generate_information()

    def to_obj(self):
        return json.dumps(self.__dict__)

    def generate_information(self):
        data = DATASET[random.randrange(0, len(DATASET))]
        dob = self.random_birthday()
        self.id = str(uuid.uuid4())
        self.name = data["name"]
        self.gender = data["gender"]
        self.dob = dob.strftime("%m/%d/%Y")
        self.age = datetime.datetime.now().year - dob.year
        self.photo = self.random_photo()

    def random_birthday(self):
        end = datetime.datetime.now() - datetime.timedelta(days=365)
        start = end - datetime.timedelta(days=(365 * 100)) 
        return start + datetime.timedelta(
            seconds=random.randint(0, int((end - start).total_seconds())),
        )

    @property
    def humanize_gender(self):
        return "woman" if self.gender == "f" else "man"

    def random_photo(self):
        output_dir = Path("downloads/{}".format(str(self.id))).absolute()
        if not Path.is_dir(output_dir):
            Path.mkdir(output_dir, parents=True)
        img_downloader = utils.image.ImageDownloader(
            query="{}, face of a {} age of {}".format(self.name, self.humanize_gender, self.age),
            limit=1, output_dir=output_dir, adult="on", timeout=60, verbose=True)
        return img_downloader.get_result_as_base64()


app = FastAPI()


@app.get("/")
async def root():
    random_people = RandomPeople()
    return {"data": json.loads(random_people.to_obj())}


@app.get("/hi")
async def root():
    return {"message": "Hi World!"}
