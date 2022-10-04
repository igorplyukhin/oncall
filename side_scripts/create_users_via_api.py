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
    def __init__(self, start, end, user1, user2):
        self.start = start
        self.end = end
        self.user1 = user1
        self.user2 = user2


months_length = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

duties = {Duty(dt.datetime(2022, 10, 1, 8, 0), dt.datetime(2022, 10, 5, 8, 0), "a.ivanov", "p.abobin")
    , Duty(dt.datetime(2022, 10, 5, 8, 0), dt.datetime(2022, 10, 10, 8, 0), "s.petrov", "b.bobrov")
    , Duty(dt.datetime(2022, 10, 10, 8, 0), dt.datetime(2022, 10, 15, 8, 0), "a.ivanov", "p.abobin")
    , Duty(dt.datetime(2022, 10, 15, 8, 0), dt.datetime(2022, 10, 20, 8, 0), "s.petrov", "b.bobrov")
    , Duty(dt.datetime(2022, 10, 20, 8, 0), dt.datetime(2022, 10, 25, 8, 0), "a.ivanov", "p.abobin")
    , Duty(dt.datetime(2022, 10, 25, 8, 0), dt.datetime(2022, 10, 30, 8, 0), "s.petrov", "b.bobrov")
    , Duty(dt.datetime(2022, 10, 30, 8, 0), dt.datetime(2022, 11, 3, 8, 0), "a.ivanov", "p.abobin")
    , Duty(dt.datetime(2022, 11, 3, 8, 0), dt.datetime(2022, 11, 8, 8, 0), "s.petrov", "b.bobrov")
    , Duty(dt.datetime(2022, 11, 8, 8, 0), dt.datetime(2022, 11, 13, 8, 0), "a.ivanov", "p.abobin")
    , Duty(dt.datetime(2022, 11, 13, 8, 0), dt.datetime(2022, 11, 18, 8, 0), "s.petrov", "b.bobrov")
    , Duty(dt.datetime(2022, 11, 18, 8, 0), dt.datetime(2022, 11, 23, 8, 0), "a.ivanov", "p.abobin")
    , Duty(dt.datetime(2022, 11, 23, 8, 0), dt.datetime(2022, 11, 28, 8, 0), "s.petrov", "b.bobrov")
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


def create_event_swapping_duty(day, user1, user2, start, end, is_swapped_parity):
    if is_swapped_parity:
        role1, role2 = "secondary", "primary"
    else:
        role1, role2 = "primary", "secondary"

    if day % 2 == 1:
        create_event(user1, start, end, role1)
        create_event(user2, start, end, role2)
    else:
        create_event(user1, start, end, role2)
        create_event(user2, start, end, role1)


def create_events():
    i_s_p = False
    for duty in duties:  # Create event for each day of duty of roster
        start_day, end_day = int(duty.start.day), int(duty.end.day)

        if start_day < end_day:
            for day in range(start_day, end_day):
                create_event_swapping_duty(
                    day, duty.user1, duty.user2, start=dt.datetime(duty.start.year, duty.start.month, day, 8, 0),
                    end=dt.datetime(duty.end.year, duty.end.month, day + 1, 8, 0), is_swapped_parity=i_s_p)
        else:  # Proceed month's shift
            for day in range(start_day, months_length[int(duty.start.month)]):  # Fill tail of month
                create_event_swapping_duty(
                    day, duty.user1, duty.user2, start=dt.datetime(duty.start.year, duty.start.month, day, 8, 0),
                    end=dt.datetime(duty.end.year, duty.start.month, day + 1, 8, 0), is_swapped_parity=i_s_p)
            # Manually add event covering 2 months
            day = months_length[int(duty.start.month)]
            create_event_swapping_duty(
                day, duty.user1, duty.user2, start=dt.datetime(duty.start.year, duty.start.month, day, 8, 0),
                end=dt.datetime(duty.end.year, duty.end.month, 1, 8, 0), is_swapped_parity=i_s_p)

            # Swap parity in case 31 end and 1 start
            if day == 31:
                i_s_p = not i_s_p

            for day in range(1, end_day):  # Fill start of new month
                create_event_swapping_duty(
                    day, duty.user1, duty.user2, start=dt.datetime(duty.end.year, duty.end.month, day, 8, 0),
                    end=dt.datetime(duty.end.year, duty.end.month, day + 1, 8, 0), is_swapped_parity=i_s_p)


if __name__ == '__main__':
    put_users_info(users)
    delete_all_events()
    create_events()
