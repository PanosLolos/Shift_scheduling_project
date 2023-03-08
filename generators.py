from random import seed, randint
import employees
from weekly_daily import *
from posts import *
from assigner import *
from scheduler import *
from datetime import date


def generate_random_employees(total, num_posts, tiers):
    list_of_employees = []
    for i in range(total):
        postmx = [randint(0, 1) for r in range(num_posts)]  # create a binary list where each digit is post eligibility
        postex = [0 for r in range(num_posts)]  # create empty post exclusion list
        if sum(postmx) == 0:
            postmx[randint(0, len(postmx) - 1)] = 1  # must have at least one post eligible
        t = randint(0, tiers)  # shuffle through contract tiers
        tempemp = employees.employee(i, postmx, postex, t)  # generate employee
        list_of_employees.append(tempemp)
    return list_of_employees


def generate_schedule_profile(start_date, end_date, etier=0):
    start = datetime.strptime(start_date, '%d/%m/%Y').date()
    end = datetime.strptime(end_date, '%d/%m/%Y').date()
    all_days = []
    for x in range(int((end - start).days) + 1):  # create a list of all dates in said given timeslot
        all_days.append(start + timedelta(x))

    r = randint(1, 100)
    own_schedule = dict()

    if r <= 50 or etier > 1:  # *********************** dedicated employee (minimal requests or occurences) ***************
        total = randint(0, int(len(all_days) / 3))
        current = 0

        for s in range(total):  # get random days for limited availability
            if current >= len(all_days) - 1:
                break
            pos = randint(current, len(all_days) - 1)
            if pos >= len(all_days) - 1:
                break
            if all_days[pos].weekday() == 6:  # considering sunday to be a non-working day
                pos += 1
            atype = randint(1, 4)
            if atype == 1:  # soft requested leave
                own_schedule[all_days[pos]] = {'type': "Soft", 'from': None, 'to': None}
                pos += 1
            elif atype == 2:  # hard leave
                extend = randint(0, 5)
                for x in range(pos, pos + extend):  # leave will be a few days but up to the end of current schedule
                    if x >= len(all_days):
                        break
                    if all_days[x].weekday() == 6:
                        continue
                    own_schedule[all_days[x]] = {'type': "Hard", 'from': None, 'to': None}
                pos += extend
            elif atype == 3:  # only from or to
                time1 = randint(9, 23)
                if time1 > 17:
                    own_schedule[all_days[pos]] = {'type': "free", 'from': None, 'to': "%d:00" % (time1)}
                else:
                    own_schedule[all_days[pos]] = {'type': "free", 'from': "%d:00" % (time1), 'to': None}
                pos += 1
            else:  # from and to
                time1 = randint(9, 15)
                time2 = randint(16, 23)
                own_schedule[all_days[pos]] = {'type': "free", 'from': "%d:00" % (time1), 'to': "%d:00" % (time2)}
                pos += 1
            current = pos

    elif r <= 65:  # *********************** parent (standard schedule, specific requests on a weekly basis) *************
        pos = 0
        if all_days[pos].weekday() == 6:  # exclude sunday
            pos += 1
        for s in range(pos, pos + 6):  # will possibly have a set request per weekday
            if all_days[s].weekday() == 6:  # skip Sunday
                continue
            atype = randint(0, 100)
            if atype < 20:  # 20% chance of having a set day off
                for d in range(0, 4):
                    dayslot = s + (d * 7)
                    if dayslot < len(all_days):  # fill all weekdays with a Soft leave
                        own_schedule[all_days[dayslot]] = {'type': "Soft", 'from': None, 'to': None}
            elif atype < 40:  # 20% chance of having a set from
                for d in range(0, 4):
                    dayslot = s + (d * 7)
                    if dayslot < len(all_days):  # fill all weekdays with a from
                        time1 = randint(9, 18)
                        own_schedule[all_days[dayslot]] = {'type': "free", 'from': "%d:00" % (time1), 'to': None}
            elif atype < 60:  # 20% chance of having a set to
                for d in range(0, 4):
                    dayslot = s + (d * 7)
                    if dayslot < len(all_days):  # fill all weekdays with a to
                        time1 = randint(18, 21)
                        own_schedule[all_days[dayslot]] = {'type': "free", 'from': None, 'to': "%d:00" % (time1)}
            elif atype < 65:  # 5% chance of requesting a leave of a few days at a certain point
                sn = s + (7 * randint(0, 3))  # random position with that starting weekday within the month
                extend = randint(0, 5)
                for x in range(sn, sn + extend):  # leave will be a few days but up to the end of current schedule
                    if x >= len(all_days):
                        break
                    if all_days[x].weekday() == 6:
                        continue
                    own_schedule[all_days[x]] = {'type': "Hard", 'from': None, 'to': None}
    elif r <= 95:  # *********************** college student (standard schedule, erratic requests) ***********************
        pos = 0
        if all_days[pos].weekday() == 6:  # exclude sunday
            pos += 1
        for s in range(pos, pos + 6):
            if all_days[s].weekday() in (5, 6):  # skip Saturday, Sunday
                continue
            atype = randint(0, 100)
            if atype < 20:
                for d in range(0, 4):
                    dayslot = s + (d * 7)
                    if dayslot < len(all_days):  # fill all weekdays with a Soft leave
                        own_schedule[all_days[dayslot]] = {'type': "Soft", 'from': None, 'to': None}
            elif atype < 40:  # 20% chance of having a set from
                for d in range(0, 4):
                    dayslot = s + (d * 7)
                    if dayslot < len(all_days):  # fill all weekdays with a from
                        time1 = randint(9, 18)
                        own_schedule[all_days[dayslot]] = {'type': "free", 'from': "%d:00" % (time1), 'to': None}
            elif atype < 60:  # 20% chance of having a set to
                for d in range(0, 4):
                    dayslot = s + (d * 7)
                    if dayslot < len(all_days):  # fill all weekdays with a to
                        time1 = randint(18, 21)
                        own_schedule[all_days[dayslot]] = {'type': "free", 'from': None, 'to': "%d:00" % (time1)}
        revents = randint(0, 5)  # add some random events
        if revents > 0:  # Random soft leaves
            for y in range(revents):
                rpos = randint(1, len(all_days) - 1)
                if all_days[rpos].weekday() == 6:  # switch sunday to saturday
                    rpos -= 1
                own_schedule[all_days[rpos]] = {'type': "Soft", 'from': None, 'to': None}
        if revents > 3:  # add two random hard single-day leaves
            rpos = randint(1, len(all_days) - 1)
            if all_days[rpos].weekday() == 6:
                if rpos < len(all_days) - 1:  # switch sunday to monday if possible
                    rpos += 1
                else:  # else switch sunday to saturday
                    rpos -= 1
            own_schedule[all_days[rpos]] = {'type': "Hard", 'from': None, 'to': None}
            # REPEAT ONCE
            rpos = randint(1, len(all_days) - 1)
            if all_days[rpos].weekday() == 6:
                if rpos < len(all_days) - 1:  # switch sunday to monday if possible
                    rpos += 1
                else:  # else switch sunday to saturday
                    rpos -= 1
            own_schedule[all_days[rpos]] = {'type': "Hard", 'from': None, 'to': None}
        if revents > 4:  # add exams leave
            rpos = randint(0, len(all_days) - 1)
            extend = randint(0, 15)
            for x in range(rpos, rpos + extend):  # leave will be a few days but up to the end of current schedule
                if x >= len(all_days):
                    break
                if all_days[x].weekday() == 6:
                    continue
                own_schedule[all_days[x]] = {'type': "Hard", 'from': None, 'to': None}
    else:  # ************************** 5% chance of random exception: end of contract, large sickness leave ***********
        rpos = randint(0, len(all_days) - 1)
        for x in range(rpos, len(all_days)):
            if x >= len(all_days):
                break
            if all_days[x].weekday() == 6:
                continue
            own_schedule[all_days[x]] = {'type': "Hard", 'from': None, 'to': None}

    result = dict()
    for key in sorted(own_schedule):  # sort dictionary by date for readability
        result[key] = own_schedule[key]
    return result


def generate_weighted_week(start, min_opening, min_closing, type=1,
                           tseed=13):  # types include: 1# retailer (9:00-21:00), 2# entertainment (variable)

    seed(tseed)
    day_dates = []
    for i in range(0, 7):
        day_dates.append(start.date() + timedelta(days=i))
    print(day_dates)
    week = weekly(day_dates[0], day_dates[-1])
    if (type == 1):  # retailer with a 9:00-21:00 schedule and Sundays off
        for d in day_dates:
            if d.weekday() != 6:  # exclude Sundays
                start_time = time(9, 0)
                end_time = time(21, 0)
                week.man_add_day(
                    generate_weighted_day(datetime.combine(d, start_time), datetime.combine(d, end_time), min_opening,
                                          min_closing))
            else:
                week.man_add_day(daily(datetime.combine(d, time(0, 0)), datetime.combine(d, time(0, 0))))
    else:  # entertainment venue with a 15:00-02:00 workday schedule and a 11:00-02:00 weekend, no days off
        for d in day_dates:
            if d.weekday() not in (5, 6):  # exclude Sundays
                start_time = time(15, 0)
                end_time = time(2, 0)
                week.man_add_day(generate_weighted_day(datetime.combine(d, start_time),
                                                       datetime.combine(d + timedelta(days=1), end_time), min_opening,
                                                       min_closing))
            else:
                start_time = time(11, 0)
                end_time = time(2, 0)
                week.man_add_day(generate_weighted_day(datetime.combine(d, start_time),
                                                       datetime.combine(d + timedelta(days=1), end_time), min_opening,
                                                       min_closing))

    return week


def generate_weighted_day(start, end, min_opening, min_closing):  # start/end need to be of form DD/MM/YYYY HH:MM

    genday = daily(start, end)
    weights = [[k, 0] for k in range(len(genday.inv))]
    baseline = randint(1, 4)  # baseline weight for a minimum of employees needed
    for i in weights:  # establish a baseline
        i[1] = baseline

    for i in range(1, 5):  # first hour is the opening, last hour is the closing
        weights[i][1] = min_opening
        weights[-(i + 1)][1] = min_closing
    weights[-1][1] = 0  # last timeslot to be zero-weighted as closing hour

    peaks = randint(0, 4)
    for i in range(1, len(weights), len(weights) // (peaks + 2)):
        if i >= len(weights) - 4:
            break
        if i not in (0, 1, 2) and i != len(weights):  # update entire hour
            peak = randint(1, 5)
            weights[i][1] += peak
            weights[i - 1][1] += peak
            weights[i + 1][1] += peak
            weights[i + 2][1] += peak

            if weights[i - 2][1] - weights[i][1] < -1:  # smooth out weights between peaks and baselines
                weights[i - 2][1] = weights[i][1] - 1
            if weights[i - 3][1] - weights[i][1] < -1:
                weights[i - 3][1] = weights[i][1] - 1
            if weights[i - 4][1] - weights[i - 3][1] < -1:
                weights[i - 4][1] = weights[i - 3][1] - 1
            if weights[i - 5][1] - weights[i - 3][1] < -1:
                weights[i - 5][1] = weights[i - 3][1] - 1

            if weights[i + 3][1] - weights[i][1] < -1:
                weights[i + 3][1] = weights[i][1] - 1
            if weights[i + 4][1] - weights[i][1] < -1:
                weights[i + 4][1] = weights[i][1] - 1
            if weights[i + 5][1] - weights[i + 4][1] < -1:
                weights[i + 5][1] = weights[i + 4][1] - 1
            if weights[i + 6][1] - weights[i + 4][1] < -1:
                weights[i + 6][1] = weights[i + 4][1] - 1

    genday.update_daily(weights)  # add the weights to the newly-created schedule
    return genday


def generate_model(start_date, total_employees, type=1):
    if type == 1:  # retailer has on average 4 posts of equal schedule times (warehouse duty purposefully excluded) avg training profile is 4 days per post
        posts = []
        for i in range(1, 4):  # initialize 3 posts.
            posts.append(post(i))
        employee_list = generate_random_employees(total_employees, 4, 3)

    else:  # cinema has on average 3 posts of slightly different schedule time, avg training profile is 2 days per post
        print("Stage 1: Initializing posts.")
        posts = []
        for i in range(0, 3):  # initialize 3 posts.
            posts.append(post(i))
        print("Posts Initialized.")
        employee_list = generate_random_employees(total_employees, 3, 2)

        print("Schedule created.\nStage 2: Generating post schedule.")
        post1week = generate_weighted_week(start_date, 2, 2, 2)
        post2week = generate_weighted_week(start_date, 2, 3, 2)
        post3week = generate_weighted_week(start_date, 1, 2, 2)
        posts[0].get_workweek(post1week)
        posts[1].get_workweek(post2week)
        posts[2].get_workweek(post3week)
        print("Schedule generated and assinged to posts.\nStage 3: Generating Random Employees.")
        employee_list = generate_random_employees(total_employees, 3, 2)
        print("Employees Assigned.\nStage 4: Generating employee availability schedule.")
        for i in employee_list:
            i.update_schedule(generate_schedule_profile(start_date.strftime('%d/%m/%Y'),
                                                        (start_date + timedelta(days=7)).strftime('%d/%m/%Y'), i.tier))
        print("Employees Assigned.\nStage 5: Generating employee availability schedule.")
        for i in employee_list:
            i.update_schedule(generate_schedule_profile(start_date.strftime('%d/%m/%Y'),
                                                        (start_date + timedelta(days=7)).strftime('%d/%m/%Y'), i.tier))
        print("Generated", len(employee_list), "employees.\nStage 6: Assigning employees to posts.")
        for i in range(0, 3):
            posts[i].get_employees(employee_list, 2)
        print("Employees assigned.")

    return posts, employee_list


def generate_tiers(n=3):  # creates a list of employees, with their tier features
    mytiers = tiers(n)
    mytiers.update_tier(0, 5, 8, 3, 5, 4.5, 0.12)  # lower tier
    mytiers.update_tier(1, 6, 8, 4, 5, 4.5, 0.12)  # middle tier
    mytiers.update_tier(2, 8, 8, 5, 6, 5)  # higher tier
    for t in mytiers.tier:
        print("--Tier:", t, "-------------------")
        for k in mytiers.tier[t]:
            print(k, ":", mytiers.tier[t][k])
    return mytiers

