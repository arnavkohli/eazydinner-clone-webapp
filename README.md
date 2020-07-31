# sample-webapp

## Usecase

- Search top 5 restaurants by location and/or cuisines (data outsourced from _eazydinner_)

- Didn't add cost filter becuase as it is the number of restaurants being displayed are significantly lower than _zomato_ and it didn't seem viable

## Hosting

Hosted on a EC2 instance 

_Home Page_ : http://ec2-18-222-18-167.us-east-2.compute.amazonaws.com/

## Local Setup

### Initialize Environment:
    python -m venv env

### Install Requirements:
    pip install -r requirements.txt
    
### Run:
    python app.py

### Tests (using selenium)
    python ./tests/test_search.py
