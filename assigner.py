from weekly_daily import *
from posts import *
from copy import deepcopy
from employees import *


class assignments:

    def __init__(self, list_of_employees, uid=0):
        self.id = uid
        self.employees = dict()
        self.start_date = None
        self.end_date = None
        for emp in list_of_employees:
            self.employees[emp.id] = dict()  # initialize each employee's schedule dict using his unique ID as key
            self.employees[emp.id]['hours'] = 0  # initialize how many hours they're set to work for the week

    def printme(self, verbose=False):
        print("--- Assignment", self.id, "---")
        print("Start:", self.start_date)
        print("End:  ", self.end_date)
        if not verbose:  # print only the employees
            for emp in self.employees:
                print("Employee", emp," with hours", self.employees[emp]['hours'])
        else:  # print employees along with their assigned schedule
            print("EmployeeID", end=' ')
            tdate = self.start_date
            while tdate <= self.end_date:
                print(tdate.date(), end=' ')
                tdate += timedelta(days=1)
            print()
            for emp in self.employees:  # prettyprint (R) to confirm initialization
                print("    ", emp, end='    ')
                for t in self.employees[emp]:
                    print("     ", self.employees[emp][t], end='    ')
                print()

    def init_assignment_schedule(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        for emp in self.employees:
            tdate = start_date
            while tdate <= end_date:
                self.employees[emp][tdate] = 'R'  # initialize all days as repos
                tdate += timedelta(days=1)


def evaluate_posts_total(posts=None, eval_type=0):  # evaluates posts on a weekly demand basis
    evaluations = []
    for p in posts:
        ev = 0
        score = 0
        cdays = 0
        for g in p.schedule.dayshifts.keys():
            cdays += 1
            l = p.evaluate(eval_type, day=g, verbose=False)
            ev += l[0]
            score += l[1]
        evaluations.append(
            [p.id, ev / cdays, score / cdays])  # store each post as: [post_id,average evaluation, average score]
    return evaluations


def evaluate_posts_day(posts=None, day=None, eval_type=0):  # evaluates posts on a daily demand basis
    evaluations = []
    for p in posts:
        l = p.evaluate(eval_type, day=day, verbose=False)
        evaluations.append([p.id, l[0], l[1]])  # store each post as: [post_id,daily evaluation, daily score]
    return evaluations


def assign(start_date=None, end_date=None, employees=None, tiers=None, posts=None, id=0):
    if start_date is None or end_date is None or employees is None or posts is None:
        print("Error: missing arguments.")
        return

    week = get_day_list(start_date, end_date)  # create a list of working days for ease of calculations
    result = assignments(employees, id)  # initialize assignments class for said dates
    result.init_assignment_schedule(start_date, end_date)

    emplist = []
    for e in employees:
        emplist.append([deepcopy(e),tiers.tier[e.tier].copy()])  # initialize temporary employees to avoid corrupting existing data
    for e in emplist:
        e[1]['Total_min'] = e[1]['min_hours'] * e[1]['min_shifts']  # leftover hours*shifts will be used for equalizing pay
        e[1]['Total_max'] = e[1]['max_hours'] * e[1]['max_shifts']

    postlist = deepcopy(posts)  # initialize temporary posts to avoid corrupting existing data

    weeklies = evaluate_posts_total(postlist)  # overall post evaluation for each week to be used as tiebreaker
    rankings = [[x.id, [], []] for x in postlist]  # post rankings are of type [postID, Daily_eval, weekly_eval]

    for day in week:
        rankings = get_rankings(day, rankings, postlist, weeklies)
        while rankings:  # while an unhandled post still exists
            post = choose_post(rankings)
            print("Matches for post", post[0], "ranked as", post[1])
            for p in posts:
                if post[0] == p.id:
                    break
            post[1] = p.evaluate(day=day)
            print("Post", post[0], "reevaluated as", post[1])
            matches = dict()
            matches = assign_employees_to_shifts(post, rankings, emplist, posts, day)
            for m in matches:
                print("Shift",m," ",matches[m])
            for m in matches:
                result.employees[matches[m]['employee']][day] = None                    # reset the placeholder
                result.employees[matches[m]['employee']][day] = dict()
                result.employees[matches[m]['employee']][day]['post'] = post[0]                 # input post ID
                result.employees[matches[m]['employee']][day]['shift']  = m                     # input shift ID
                result.employees[matches[m]['employee']][day]['duration'] = matches[m]['duration'] # input shift duration

            for r in rankings:  # remove handled post
                if post[0] == r[0]:
                    rankings.remove(r)

    return result


def assign_employees_to_shifts(chosen=None, rankings=None, emps=None, posts=None, day=None):
    if chosen is None or rankings is None or emps is None or posts is None or day is None:
        print("Error: missing arguments.")
        return

    for post in posts:
        if chosen[0] == post.id:
            break
    shifts = post.schedule.dayshifts[day]  # keep track of only that day's shifts

    match = dict()
    if chosen[1][0] == 2:  # Adequate available employees: set-covering for performance
        for s in shifts:
            match[s.id] = dict()
            match[s.id]['employee'] = None
            duration = s.duration / 4  # convert timeslot duration into hours
            hour_diff = 100  # initialize first criterion: matching minimum hours to shift
            min_hours_left = 0  # initialize second criterion: equalizing pay
            for e in emps:
                if e[1]['max_shifts'] <= 0:  # ignore employees who have fulfilled their shifts
                    continue
                if e[0].id in post.available[day]:  # check only available employees
                    if abs(e[1]['min_hours'] - duration) < hour_diff:  # smaller difference in hours needed and provided
                        if e[1]['Total_min'] > min_hours_left:  # tie breaker: prefer one with less total hours so far
                            hour_diff = abs(e[1]['min_hours'] - duration)
                            min_hours_left = e[1]['Total_min']
                            match[s.id]['employee'] = e[0].id  # find the best matching employee
                            match[s.id]['duration'] = duration
            for e in emps:
                if e[0].id == match[s.id]['employee']:  # update employee list with the appropriate shift
                    e[1]['min_shifts'] -= 1
                    e[1]['max_shifts'] -= 1
                    e[1]['min_hours'] -= duration
                    e[1]['max_hours'] -= duration
                    break
            # post.available[day].remove(e[0].id)                 # remove the employee from that day's availability list
            for p in posts:
                if e[0].id in p.available[day]:
                    p.available[day].remove(e[0].id)  # remove the employee from that day's availability list

    else:  # Adequate with soft-unavailable employees: set-covering for performance
        sorted_shifts = sort_shifts_for_min_coverage(post, day)
        for s in sorted_shifts:  # proceed for as many shifts as possible with employees available as if on performance
            match[s.id] = dict()
            print("Match:", s.id)
            match[s.id]['employee'] = None
            duration = s.duration / 4  # convert timeslot duration into hours
            hour_diff = 100  # initialize first criterion: matching minimum hours to shift
            min_hours_left = 0  # initialize second criterion: equalizing pay
            for e in emps:
                if e[1]['max_shifts'] <= 0:  # ignore employees who have fulfilled their shifts
                    continue
                if e[0].id in post.available[day]:  # check only available employees
                    if abs(e[1]['min_hours'] - duration) < hour_diff:  # smaller difference in hours needed and provided
                        if e[1]['Total_min'] > min_hours_left:  # tie breaker: prefer one with less total hours so far
                            hour_diff = abs(e[1]['min_hours'] - duration)
                            min_hours_left = e[1]['Total_min']
                            match[s.id]['employee'] = e[0].id  # find the best matching employee
                            match[s.id]['duration'] = duration
            for e in emps:
                if e[0].id == match[s.id]['employee']:  # update employee list with the appropriate shift
                    e[1]['min_shifts'] -= 1
                    e[1]['max_shifts'] -= 1
                    e[1]['min_hours'] -= duration
                    e[1]['max_hours'] -= duration
                    break
            # post.available[day].remove(e[0].id)                 # remove the employee from that day's availability list
            for p in posts:
                if e[0].id in p.available[day]:
                    p.available[day].remove(e[0].id)  # remove the employee from that day's availability list

            if not p.available[day]:  # when all available employees are set, move on to the soft unavailable
                break
        temp = s  # continue with the unassigned shifts
        unassigned = False
        for s in shifts:
            if s.id != temp.id and not unassigned:  # until s reaches temp in the list, continue
                continue
            elif s.id == temp.id:  # pass over temp once.
                unassigned = True
                continue

            for e in emps:
                if e[1]['max_shifts'] <= 0:  # ignore employees who have fulfilled their shifts
                    continue
                if e[0].id in post.soft_unavailable[day]:  # check only available employees
                    if e[0].schedule[day]['type'] == 'free':  # if the employee's availability allows him to work that day
                        if e[0].schedule[day]['from'] is not None and e[0].schedule[day]['to'] is None:  # availability FROM only
                            if s.start >= get_timeslot(e[0].schedule[day]['from'], post, day):  # for skeleton crews no extra criteria will be required
                                match[s.id]['employee'] = e[0].id  # find the best matching employee
                                match[s.id]['duration'] = duration
                                e[1]['min_shifts'] -= 1
                                e[1]['max_shifts'] -= 1
                                e[1]['min_hours'] -= duration
                                e[1]['max_hours'] -= duration
                                for p in posts:
                                    p.soft_available[day].remove(e[0].id)  # remove the employee from that day's availability list
                        elif e[0].schedule[day]['to'] is not None and e[0].schedule[day]['from'] is None:  # availability TO only
                            if s.start <= get_timeslot(e[0].schedule[day]['to'], post,
                                                       day):  # for skeleton crews no extra criteria will be required
                                match[s.id]['employee'] = e[0].id  # find the best matching employee
                                match[s.id]['duration'] = duration
                                e[1]['min_shifts'] -= 1
                                e[1]['max_shifts'] -= 1
                                e[1]['min_hours'] -= duration
                                e[1]['max_hours'] -= duration
                                for p in posts:
                                    p.soft_available[day].remove(e[0].id)  # remove the employee from that day's availability list
                        elif e[0].schedule[day]['to'] is not None and e[0].schedule[day]['from'] is not None:  # availability FROM AND TO
                            if get_timeslot(e[0].schedule[day]['to'], post, day) >= s.start >= get_timeslot(
                                    e[0].schedule[day]['from'], post, day):
                                match[s.id]['employee'] = e[0].id  # find the best matching employeematch[s.id]['employee'] = e[0].id  # find the best matching employee
                                match[s.id]['duration'] = duration
                                e[1]['min_shifts'] -= 1
                                e[1]['max_shifts'] -= 1
                                e[1]['min_hours'] -= duration
                                e[1]['max_hours'] -= duration
                                for p in posts:
                                    p.soft_available[day].remove(e[0].id)  # remove the employee from that day's availability list
            if chosen[1][0] == 0:  # full unavailable employees will be included to fill as many shifts as possible
                if s.id not in match.keys():  # if no one adequate was found:
                    for e in emps:
                        if e[1]['max_shifts'] <= 0:  # ignore employees who have fulfilled their shifts
                            continue
                        if e[0].id in post.soft_unavailable[day]:  # check only available employees
                            if e[0].schedule[day]['type'] == 'Soft':  # if the employee's availability allows him to work that day
                                match[s.id]['employee'] = e[0].id  # find the best matching employee
                                match[s.id]['duration'] = duration
                                e[1]['min_shifts'] -= 1
                                e[1]['max_shifts'] -= 1
                                e[1]['min_hours'] -= duration
                                e[1]['max_hours'] -= duration
                                for p in posts:
                                    if e[0].id in p.available[day]:
                                        p.soft_available[day].remove(e[0].id)  # remove the employee from that day's availability list

    return match


def get_timeslot(etime=None, post=None, day=None):  # assign timeslot based on time for particular day and post
    delta = day - post.workweek.datestart
    found = deepcopy(post.workweek.days[delta.days])
    for slot in found.inv:
        if slot.atime == datetime.strptime(etime, "%H:%M").time():      #convert time given to timeslot
            return slot.timeslot



def get_rankings(day=None, rankings=None, posts=None, weeklies=None):  # function stores remaining posts for that day
    if day is None or rankings is None or posts is None or weeklies is None:
        print("Error: missing arguments.")
        return
    for r in rankings:  # always initialize remaining posts for that day
        for p in posts:
            if p.id == r[0]:
                r[1] = p.evaluate(day=day)
        for w in weeklies:  # store weekly rankings on remaining posts
            if w[0] == r[0]:
                r[2] = [w[1], w[2]]
                break
    return rankings  # list of lists [postID, [Daily_Type, Daily_Eval], [Weekly_Type,Weekly_Eval]]


def choose_post(rankings=None):  # rank posts based on shift coverage availability
    if rankings is None:
        print("Error: missing arguments.")
        return
    daily_type = 3
    daily_min = 10e5
    weekly_type = -1
    weekly_min = 10e5
    result = -1
    for r in rankings:  # find the lowest ranking post
        if r[1][0] < daily_type:  # Priority: daily availability stage of employees
            daily_type = r[1][0]
            daily_min = r[1][1]
            weekly_type = r[2][0]
            weekly_min = r[2][1]
            result = r
        elif r[1][0] == daily_type:  # Tie breaker 1: daily availability against shifts to fill
            if r[1][1] < daily_min:
                daily_type = r[1][0]
                daily_min = r[1][1]
                weekly_type = r[2][0]
                weekly_min = r[2][1]
                result = r
            elif r[1][1] == daily_min:  # Tie breaker 2: average weekly availability stage of employees
                if r[2][0] < weekly_type:
                    daily_type = r[1][0]
                    daily_min = r[1][1]
                    weekly_type = r[2][0]
                    weekly_min = r[2][1]
                    result = r
                elif r[2][1] < weekly_min:  # Tie breaker 3: average weekly availability against shifts to fill
                    daily_type = r[1][0]
                    daily_min = r[1][1]
                    weekly_type = r[2][0]
                    weekly_min = r[2][1]
                    result = r
    return result  # list of lists [postID, [Daily_Type, Daily_Eval], [Weekly_Type,Weekly_Eval]]


def min_shifts_required(post=None, day=None):  # min shift coverage solver for skeleton-crew scheduling
    delta = day - post.workweek.datestart
    found = deepcopy(post.workweek.days[delta.days])
    shifts = deepcopy(post.schedule.dayshifts[day])
    sorted_shifts = []
    not_assigned = len(shifts)  # counter to ensure all shifts have been sorted
    while not_assigned > 0:
        minimum_slot = None
        minimum_weight = 10e5  # criterion: lowest weight (most needed shift)
        to_remove = None
        for slot in found.inv:
            if minimum_weight > slot.weight > 0:  # find the minimum weight > 0
                minimum_slot = slot.timeslot
                minimum_weight = slot.weight
        if minimum_slot is None:                # if minimum slot is empty, all weights <= 0, remaining shifts can be sorted based on duration
            max_duration = 0
            for idx,candidate in enumerate(shifts):
                if candidate.duration > max_duration:
                    to_remove = idx
                    max_duration = candidate.duration
            sorted_shifts.append(shifts[to_remove])
            print("Assigned3:", candidate.id, "with start", candidate.start, "and end", candidate.end)
            del shifts[to_remove]
            not_assigned -= 1
            continue
        if minimum_weight < 2:  # unique candidate shift exists
            for idx,candidate in enumerate(shifts):
                if candidate.start <= minimum_slot <= candidate.end+1:
                    to_remove = idx  # ensure that the shift will be removed from the list
                    sorted_shifts.append(candidate)
                    print("Assigned1:", candidate.id, "with start", candidate.start, "and end", candidate.end)
                    for s in found.inv:
                        if candidate.start <= s.timeslot <= candidate.end + 1:
                            s.weight -= 1  # reduce all affected weights by 1
                    break

            del shifts[to_remove]
        else:  # multiple candidates
            max_duration = 0  # Tie breaker: longest duration -> max coverage
            for idx,candidate in enumerate(shifts):
                if candidate.start <= minimum_slot <= candidate.end + 1:
                    if candidate.duration > max_duration:
                        to_remove = idx
                        max_duration = candidate.duration
            print("Assigned2:", candidate.id, "with start", candidate.start, "and end", candidate.end)
            sorted_shifts.append(shifts[to_remove])
            for s in found.inv:  # reduce affected weights
                if sorted_shifts[-1].start <= s.timeslot <= sorted_shifts[-1].end + 1:
                    s.weight -= 1

            del shifts[to_remove]  # remove candidate
        not_assigned -= 1

    return sorted_shifts  # list of shift types


def sort_shifts_for_min_coverage(post=None, day=None):      # sorts shifts for maximum coverage
    delta = day - post.workweek.datestart
    found = deepcopy(post.workweek.days[delta.days])            #get particular post's intervals for that day
    intervals_left = dict()
    for slots in found.inv:
        intervals_left[slots.timeslot] = 0         #initialize a list of all active slots and mark them as uncovered (0)
    shifts = deepcopy(post.schedule.dayshifts[day])
    sorted_shifts = []                                          #initialize sorted shift list
    not_assigned = len(shifts)              # counter to ensure all shifts have been sorted
    to_remove = None
    while not_assigned>0:                   # 1st criterion: maximum coverage
        max_covered = 0
        to_remove = None
        for idx,s in enumerate(shifts):
            starting_point = s.start        #initialize interval starting and ending points
            ending_point = s.end
            count_covered = 0
            for i in range(starting_point+1,ending_point+1):        # count overlap with uncovered intervals
                if intervals_left[i] == 0:
                    count_covered += 1
            if count_covered > max_covered:             # find maximum coverage
                to_remove = idx
                max_covered = count_covered
        if to_remove is None:                # maximum coverage has been achieved and count_covered is now 0 for remaining shifts
            break
        sorted_shifts.append(shifts[to_remove])     # append next shift and remove it from the existing list

        for i in range(shifts[to_remove].start+1,shifts[to_remove].end+1):
            intervals_left[i] = 1
        del shifts[to_remove]
        not_assigned -= 1
    while not_assigned > 0:                # 2nd criterion: longest duration for remaining shifts
        max_duration = 0
        for idx,s in enumerate(shifts):    # maximum coverage has been achieved and remaining shifts exist
            if s.duration > max_duration:
                max_duration = s.duration
                to_remove = idx
        sorted_shifts.append(shifts[to_remove])  # append next shift and remove it from the existing list
        for i in range(shifts[to_remove].start+1,shifts[to_remove].end+1):
            intervals_left[i] = 1
        del shifts[to_remove]
        not_assigned -= 1
    return sorted_shifts
