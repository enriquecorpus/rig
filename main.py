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
        }

    def generate_information(self):
        data = dataset[random.randrange(0, len(dataset))]
        self.name = data["name"]
        self.gender = data["gender"]
        self.dob = self.random_birthday()

    def random_birthday(self):
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=(365 * 100)) 
        return (start + datetime.timedelta(
            seconds=random.randint(0, int((end - start).total_seconds())),
        )).strftime("%m/%d/%Y")


    

app = FastAPI()


@app.get("/")
async def root():
    random_people = RandomPeople()

    return {"data": random_people.toJSON()}

@app.get("/hi")
async def root():
    return {"message": "Hi World!"}  