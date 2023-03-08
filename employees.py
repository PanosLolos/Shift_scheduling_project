class employee:     #employee class contains their ID, post eligibility, contract tier and weekly availability schedule

    def __init__(self, uid, aposts, eposts, ctier = 0):
        self.id = uid
        self.posts = aposts
        self.post_exclusions = eposts
        self.tier = ctier
        self.schedule = dict()

    def update_posts(self, pos, val):
        self.posts[pos] = val

    def update_post_exclusions(self, pos, val):
        self.post_exclusions[pos] = val

    def update_schedule(self, newschedule):     #allows
        self.schedule.update(newschedule)

    def printme(self,verbose=False):        #verbose parameter prints their availability schedule as a dictionary
        print("Employee", self.id, "- Tier", self.tier)
        print("Post Eligiblity:")
        for x in range(len(self.posts)):
            print(x, end=' ')
        print()
        for x in self.posts:
            print(x, end=' ')
        print()
        if verbose:
            self.print_schedule()

    def print_schedule(self):
        print("Schedule for employee", self.id)
        for k in self.schedule.keys():
            print(k,":",self.schedule[k])

    def modify_repo_days(self, dateslist):
        for d in dateslist:
            self.schedule[d] = {'type': "Hard", 'from': None, 'to': None}

class tiers:        # tiers stored in dictionary and may be updated manually

    def __init__(self,number):
        self.tier = dict()
        for t in range(0,number):
            self.tier[t] = dict()

    def update_tier(self,t, min_hours, max_hours,min_shifts,max_shifts, pay_per_hour, extra=0):
        self.tier[t]['min_hours'] = min_hours
        self.tier[t]['max_hours'] = max_hours
        self.tier[t]['min_shifts'] = min_shifts
        self.tier[t]['max_shifts'] = max_shifts
        self.tier[t]['pay_per_hour'] = pay_per_hour
        self.tier[t]['extra'] = extra




