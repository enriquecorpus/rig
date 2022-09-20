from fastapi import FastAPI
import csv
import random
import datetime

reader = csv.reader(open('names.csv', 'r'))
dataset = {}
for i,row in enumerate(reader):
   name, gender,_,_ = row
   dataset[i] = {
       "name": name,
       "gender": gender,
   }


class RandomPeople():
    def __init__(self):
        self.generate_information()

    def toJSON(self):
        return {
            "name" : self.name,
            "gender": self.gender,
            "dob" : self.dob,
            "photo": self.random_photo()
        }

    def generate_information(self):
        data = dataset[random.randrange(0, len(dataset))]
        self.name = data["name"]
        self.gender = data["gender"]
        self.dob = self.random_birthday()
        self.photo = self.random_photo()

    def random_birthday(self):
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=(365 * 100)) 
        return (start + datetime.timedelta(
            seconds=random.randint(0, int((end - start).total_seconds())),
        )).strftime("%m/%d/%Y")

    @property
    def humanize_gender(self):
        return "woman" if self.gender == "f" else "man"
    def random_photo(self):
        # of images to download. ("tall, square, wide, panoramic")
        import pdb
        pdb.set_trace()
        arguments = {"keywords": "face of a {}".format(self.gender),
                    "format": "jpg",
                    "limit":4,
                    "print_urls":True,
                    "size": "medium",
                    "aspect_ratio":"panoramic"}
        x = response.download(arguments)


    

app = FastAPI()


@app.get("/")
async def root():
    random_people = RandomPeople()

    return {"data": random_people.toJSON()}

@app.get("/hi")
async def root():
    return {"message": "Hi World!"}  