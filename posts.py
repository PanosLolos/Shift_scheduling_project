from employees import *
from datetime import datetime, timedelta

maxwh = 8
minwh = 5

class post:

    def __init__(self, pid):
        self.id = pid               # posts are assigned an incremental integer ID
        self.available = dict()         # weekly list of available employees for each day
        self.soft_unavailable = dict()  # weekly list of soft_unavailable employees for each day
        self.trainable = dict()          # weekly list of post-eligible employees who can be trained to post
        self.workweek = None
        self.schedule = None             # schedule contains the shift solution as calculated by the scheduler
        self.params = dict()

    def get_workweek(self,schedule,params_dict):  #get the weekly schedule
        self.workweek = schedule
        self.available = dict()             #re-initialize dictionaries for information validity
        self.soft_unavailable = dict()
        self.trainable = dict()
        self.params = params_dict.copy()
        for d in self.workweek.days:        #create empty lists for each workweek day
            self.available[d.date] = []
            self.soft_unavailable[d.date] = []
            self.trainable[d.date] = []


    def get_employees(self,employees_list,min_train):   #requires an existing workweek to function properly
        for emp in employees_list:
            if emp.posts[self.id] == 1:             # for post eligible employees, get their availability per day
                for d in self.available.keys():     # iterate through the week
                    if d in emp.schedule.keys():
                        if emp.schedule[d]['type'] != 'Hard':
                            self.soft_unavailable[d].append(emp.id)  # keep soft_unavailable employees in standby option
                        else:
                            continue              # hard_unavailable employees are excluded
                    else:
                        self.available[d].append(emp.id)      # if employee has no unavailability on that day, save him
            elif emp.post_exclusions[self.id] != 1:               # prospect trainee feature for non excluded employees

                for d in self.available.keys():     # date must ensure that employee will be able to work for min_train days
                    if d in emp.schedule.keys():
                        if emp.schedule[d]['type'] == 'Hard': #ensure prospect trainee can work for min_train days
                            continue
                        else:
                            td = d
                            eligible = True
                            for xd in range(1,min_train):
                                td = td+timedelta(days=1)
                                if td in emp.schedule.keys():
                                    if emp.schedule[td]['type'] =='Hard':
                                        eligible = False
                                        break
                            if eligible:                # assign employee id to training starting day only.
                                self.trainable[d].append(emp.id)
                    else:
                        td = d
                        eligible = True
                        for xd in range(1, min_train):
                            td = td + timedelta(days=1)
                            if td in emp.schedule.keys():
                                if emp.schedule[td]['type'] == 'Hard':
                                    eligible = False
                                    break
                        if eligible:  # assign employee id to training starting day only.
                            self.trainable[d].append(emp.id)

    def printme(self,verbose=False):
        print("- Post", self.id," -------------------")
        print("- Total Availability - ")
        for k in self.available.keys():
            print("-      Day:", k, self.available[k])
        print("\n- Total Soft Unavailable - ")
        for k in self.soft_unavailable.keys():
            print("-      Day:", k, self.soft_unavailable[k])
        print("\n- Total Trainable - ")
        for k in self.trainable.keys():
            print("-      Day:", k, self.trainable[k])
        if verbose:
            print("\n- Workweek -")
            self.workweek.printme()
            print("\n - Solved Shifts -")
            self.schedule.printme(verbose=verbose)

    def evaluate(self, evaluation_type=0, day=None,verbose=False):   #evaluation types {0: total emps, 1:av emps/shifts, 2: workhours} on a daily basis

        if self.workweek is None or self.schedule is None:
            return 0

        if evaluation_type == 0:        # available employees/total shifts
            total_shifts = len(self.schedule.dayshifts[day])
            available_emps = len(self.available[day])
            soft_unav_emps = len(self.soft_unavailable[day])
            if verbose:
                print("Evaluating available employees vs total shifts needed.")
                print("Available emps:       ", available_emps)
                print("Soft-unavailable emps:", soft_unav_emps)
                print("Total Shifts Needed:  ", total_shifts)
            if total_shifts-available_emps<0:
                return [2,available_emps/total_shifts]                  # 2: performance crew. More than enough available
            elif total_shifts-(available_emps+soft_unav_emps)<0:
                return [1, (available_emps+soft_unav_emps)/total_shifts] # 1: semi-performance crew. Can't ensure unavailable demands
            else:
                return [0, (available_emps+soft_unav_emps)/total_shifts] # 0: skeleton crew. Not enough people to cover

        else:      # total available workhours/total needed workhours
            total_workhours = 0
            for s in self.schedule.dayshifts[day]:
                total_workhours += (s.duration/4)
            total_available_wh = len(self.available) * maxwh
            total_soft_av_wh = len(self.soft_unavailable) * maxwh
            if verbose:
                print("Evaluating available workhours vs total shift duration.")
                print("Available workhours:    ", total_available_wh)
                print("Extra dragged workhours:", total_soft_av_wh)
                print("Total shift duration:   ", total_workhours)
            if total_workhours - total_available_wh < 0:
                return [2, total_available_wh/total_workhours]          # 2: performance crew. enough workhours available
            elif total_workhours - (total_soft_av_wh+total_available_wh) < 0:
                return [1, (total_soft_av_wh+total_available_wh)/total_workhours] # 1: semi-performance crew. Workhours will need to be dragged
            else:
                return [0, (total_soft_av_wh+total_available_wh)/total_workhours] # 0: skeleton crew. Not enough workhours












