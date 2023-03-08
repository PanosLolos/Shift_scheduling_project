from datetime import time,timedelta,datetime
import calendar
import numpy as np


class weekly: #weekly schedule is initialized using just a start/end date

    def __init__(self,dstart,dend):
        self.days = []
        self.datestart = dstart
        self.dateend = dend

    def build_week(self,dailies): # to build the daily schedule array, there need to be daily start-end hours and their respective weights in separate lists
        for d in dailies:
            self.days.append(d)

    def man_add_day(self,day):
        self.days.append(day)

    def get_total_workhours(self):
        dwh = 0
        for d in self.days:
            dwh += d.get_total_workhours()
        return dwh

    def get_avg_daily_workhours(self):
        awh = 0
        week = 7
        for d in self.days:
            if d.get_total_workhours()==0:
                week-=1
            else:
                awh+=d.get_total_workhours()
        return awh/week


    def printme(self,verbose=0):    #printme function
        print("Week:",self.datestart,"-",self.dateend)
        if(verbose==0):
            for d in self.days:
                print("Day:",d.dayname," Start:",d.inv[0].atime,"End:",d.inv[-1].atime)
        else:
            for d in self.days:
                d.printme()
            print("Daily Workhours:")
            for d in self.days:
                print("Day:",d.dayname," Total:",d.get_total_workhours(),"Average:", d.get_average_weight())
            print("Total Weekly Workhours: ", self.get_total_workhours())
            print("Average Daily Workhours:", self.get_avg_daily_workhours())



class daily:  # daily schedule is initialized using just the start/end hours and splitting the timeslot into quarter intervals

    def __init__(self, dstart,dend):
        self.dayname = calendar.day_name[dstart.weekday()] #assign weekday based on start date, end date may be the next day if after 23:59
        self.inv= []
        self.date = dstart.date()
        intervals = get_interval_list(dstart,dend,15)
        slotkey = 1
        for i in intervals:
            self.inv.append(quarter(slotkey,i))
            slotkey +=1

    def update_daily(self, weights=[0,0]):  #update the weights of each timeslot based on the given vector
        for x in weights:
            self.inv[x[0]].update_weight(x[1])

    def get_total_workhours(self): # sum the weights of the day
        wh = 0
        for x in self.inv:
            wh+=x.weight
        return wh/4

    def get_average_weight(self): # average the weights of the day per timeslot
        awh = 0
        for x in self.inv:
            awh+=x.weight
        return awh/len(self.inv)

    def printme(self,verbose=0):
        print("Day:",self.dayname,self.date)
        for t in self.inv:
            t.printme(verbose=verbose)


class quarter: #quarter object contains the timeslot id, the time and an integer weight

    def __init__(self,slotkey,qtime,w=0):
        self.timeslot = slotkey
        self.atime = qtime
        self.weight = w     # weight is an indicator of how many workers are needed in that timeslot
        self.people = []

    def update_weight(self,neww):
        self.weight = neww

    def add_worker(self,workername):
        self.weight -=1
        self.people.append(workername)

    def printme(self,verbose=0):
        print("Timeslot:",self.timeslot,"Time:",self.atime,"Weight:",self.weight)
        if(verbose!=0):
            print("Workers:",end=' ')
            for x in self.people:
                print(x,end=' ')

            print()

def get_interval_list(starttime,endtime,inv): #inv must be an integer in minutes
    intervals = []
    current = starttime
    while(current < endtime):
        intervals.append(current.time())
        current = current + timedelta(minutes=inv)
    intervals.append(endtime.time())
    return intervals

def get_day_list(start_date=None,end_date=None):
    result = []
    temp_date = start_date
    while temp_date <= end_date:
        result.append(temp_date)
        temp_date += timedelta(days=1)
    return result

