from sql_requests import Requests

db = Requests('timetable.db')

def hello():
    print(db.get_teachers())

if __name__ == '__main__':
    hello()