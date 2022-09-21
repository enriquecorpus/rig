from fastapi import FastAPI
import csv
import random
import datetime
import uuid
import base64
import os
from pathlib import Path
from bing_image_downloader import bing as b


reader = csv.reader(open('names.csv', 'r'))
dataset = {}
for i, row in enumerate(reader):
    name, gender, _, _ = row
    dataset[i] = {
        "name": name,
        "gender": gender,
    }


class RandomPeople:
    id = ""
    name = ""
    gender = ""
    dob = ""
    photo = ""
    age = 0

    def __init__(self):
        self.generate_information()

    def to_json(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "dob": self.dob,
            "age": self.age,
            "photo": self.photo
        }

    def generate_information(self):
        data = dataset[random.randrange(0, len(dataset))]
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
        output_dir = Path(str(self.id)).absolute()
        if not Path.is_dir(output_dir):
            Path.mkdir(output_dir, parents=True)
        bing = b.Bing(query="face of a {} age of {}".format(self.humanize_gender, self.age),
                      limit=1, output_dir=output_dir, adult="on", timeout=60,filter="imagesize-small")
        bing.run()
        file = os.listdir(output_dir)[0]
        with open(Path(output_dir).joinpath(file).absolute(), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")




app = FastAPI()

@app.get("/")
async def root():
    random_people = RandomPeople()
    return {"data": random_people.to_json()}

@app.get("/hi")
async def root():
    return {"message": "Hi World!"}  