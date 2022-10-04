import json
import datetime as dt
import requests as r

base_url = "http://0.0.0.0:8080/api/v0"
base_users_url = base_url + "/users"
base_teams_url = base_url + "/teams"
base_events_url = base_url + "/events"
headers = {'Content-Type': 'application/json; charset=utf-8'}


class User:
    def __init__(self, login, contacts: dict, name, full_name, time_zone, active):
        self.login = login
        self.contacts = contacts
        self.name = name
        self.full_name = full_name
        self.time_zone = time_zone
        self.active = active

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Duty:
    def __init__(self, start, end, primary, secondary):
        self.start = start
        self.end = end
        self.primary = primary
        self.secondary = secondary


months_length = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

duties = {Duty(dt.datetime(2022, 10, 1, 8, 0), dt.datetime(2022, 10, 5, 8, 0), "a.ivanov", "p.abobin")
    , Duty(dt.datetime(2022, 10, 5, 8, 0), dt.datetime(2022, 10, 10, 8, 0), "p.abobin", "s.petrov")
    , Duty(dt.datetime(2022, 10, 10, 8, 0), dt.datetime(2022, 10, 15, 8, 0), "s.petrov", "a.ivanov")
    , Duty(dt.datetime(2022, 10, 15, 8, 0), dt.datetime(2022, 10, 20, 8, 0), "a.ivanov", "p.abobin")
    , Duty(dt.datetime(2022, 10, 20, 8, 0), dt.datetime(2022, 10, 25, 8, 0), "p.abobin", "s.petrov")
    , Duty(dt.datetime(2022, 10, 25, 8, 0), dt.datetime(2022, 10, 30, 8, 0), "s.petrov", "a.ivanov")
    , Duty(dt.datetime(2022, 10, 30, 8, 0), dt.datetime(2022, 11, 3, 8, 0), "a.ivanov", "p.abobin")
    , Duty(dt.datetime(2022, 11, 3, 8, 0), dt.datetime(2022, 11, 8, 8, 0), "p.abobin", "s.petrov")
    , Duty(dt.datetime(2022, 11, 8, 8, 0), dt.datetime(2022, 11, 13, 8, 0), "s.petrov", "a.ivanov")
    , Duty(dt.datetime(2022, 11, 13, 8, 0), dt.datetime(2022, 11, 18, 8, 0), "a.ivanov", "p.abobin")
    , Duty(dt.datetime(2022, 11, 18, 8, 0), dt.datetime(2022, 11, 23, 8, 0), "p.abobin", "s.petrov")
    , Duty(dt.datetime(2022, 11, 23, 8, 0), dt.datetime(2022, 11, 28, 8, 0), "s.petrov", "a.ivanov")
    , Duty(dt.datetime(2022, 11, 28, 8, 0), dt.datetime(2022, 12, 2, 8, 0), "a.ivanov", "p.abobin")}

users = [User("s.petrov", {"call": "+1 222-222-2222",
                           "email": "a@student.com",
                           "slack": "slackk",
                           "sms": "+7 111-111-1111"}, "serg", "sergey petrov", "Europe/Moscow", 1)
    , User("a.ivanov", {"call": "+1 222-222-2222",
                        "email": "b@student.com",
                        "slack": "slackk",
                        "sms": "+7 111-111-1111"}, "alex", "alex ivanov", "Europe/Moscow", 1)
    , User("b.bobrov", {"call": "+1 222-222-2222",
                        "email": "c@student.com",
                        "slack": "slackk",
                        "sms": "+7 111-111-1111"}, "boris", "boris bobrov", "Europe/Moscow", 1)
    , User("p.abobin", {"call": "+1 222-222-2222",
                        "email": "d@student.com",
                        "slack": "slackk",
                        "sms": "+7 111-111-1111"}, "petr", "petr abobin", "Europe/Moscow", 1)
         ]


def create_user(name):
    data = {"name": name}
    resp = r.post(url=f"{base_users_url}", json=data, headers=headers)
    return resp.json()


def get_users():
    resp = r.get(url=base_users_url)
    return resp.json()


def create_many_users(users):
    for u in users:
        print(create_user(u.name))


def put_users_info(users):
    for u in users:
        j = {
            "contacts": u.contacts,
            "full_name": u.full_name,
            "time_zone": u.time_zone,
            "active": u.active
        }
        url = base_users_url + "/" + u.login
        resp = r.put(url=url, headers=headers, json=j)
        print(resp)


def get_teams():
    resp = r.get(url=base_teams_url, headers=headers)
    return resp.json()


def get_events(team):
    resp = r.get(url=base_events_url + "?team=" + team)
    return resp.json()


def delete_all_events():
    for e in get_events("first_team"):
        id = str(e["id"])
        resp = r.delete(base_events_url + "/" + id, headers=headers)


def create_event(user, start, end, role):
    j = {
        "role": role,
        "start": int(start.strftime('%s')),
        "end": int(end.strftime('%s')),
        "team": "first_team",
        "user": user
    }

    resp = r.post(url=base_events_url, headers=headers, json=j)
    return resp


def create_events():
    for duty in duties:
        create_event(duty.primary, duty.start, duty.end, "primary")
        create_event(duty.secondary, duty.start, duty.end, "secondary")


if __name__ == '__main__':
    put_users_info(users)
    delete_all_events()
    create_events()

