from weekly_daily import *

def daily_solver(weekday, hourly, minimum_hrs, maximum_hrs, extra=None):
    daily = []
    min = minimum_hrs * 4 #in quarters
    max = maximum_hrs * 4 #in quarters


    result = []

    for x in weekday.inv:  # will experiment on dummy schedule of type [TIMESLOT_ID,WEIGHT,NUMBER OF ELIGIBLE SHIFTS]
        daily.append([x.timeslot, x.weight, 0])

    index = 0
    shift_id = 0
    print(daily[index])
    while (index > -1 and index<len(daily)-1):
        if daily[index][2] < daily[index][1]: #if not enough eligible shifts to cover the weight, can only create new
            shift_id+=1
            if index < (len(daily) - min-1):   # if there's space in the weekday to create a full-min shift
                new_shift = shift(shift_id,index,index+min, min)
                for i in range((index + min), (index + max)):  # update eligible shifts after current
                    if i >= len(daily): break
                    daily[i][2] += 1
                for i in range(index, (index + min)):  # update weight
                    daily[i][1] -= 1
            else:                            # if not enough space in the remaining weekday to create a full-min shift
                new_shift = shift(shift_id,len(daily)-min-1,len(daily)-1,min)
                for i in range(len(daily)-1-min,len(daily)-1):
                    daily[i][1] -=1
            print("Created shift",new_shift.id, "Start:",new_shift.start, "End:", new_shift.end)
            result.append(new_shift)
        else:   #if there are eligible shifts to cover the weight
            create_gain = 0
            if index+min> len(daily)-1:
                nidx = len(daily)-1-min
            else:
                nidx = index
            for x in range(nidx,nidx+min):    #check the gain of creating a new shift
                if(daily[x][1]-1>=0):
                    create_gain +=1

            create_gain = create_gain/(hourly*min) #gain will be [total weights covered]/[shift minimum cost]
            min_ext = max-min
            for ts in range(len(result)):
                if (index-result[ts].end) <= min_ext and (index-result[ts].end)>0 and result[ts].duration<max:
                    min_ext = (index-result[ts].end) #find the minimum extension possible
            if extra is not None:
                extend_gain = (min_ext/4)/ ((min_ext/4)* (hourly + hourly * extra))
            else:
                extend_gain = (min_ext/4)/ ((min_ext/4)*hourly)
            print("Index:", index,"Min_ext:", min_ext,"Create: ", create_gain, " VS Extend: ", extend_gain)

            if create_gain>extend_gain:             # if creating a new shift has a higher gain, create it
                shift_id += 1
                if index < (len(daily) - min - 1):  # if there's space in the weekday to create a full-min shift
                    new_shift = shift(shift_id, index, index + min, min)
                    for i in range((index + min), (index + max) - 1):  # update eligible shifts after current
                        if i >= len(daily): break
                        daily[i][2] += 1
                    for i in range(index, (index + min)):  # update weight
                        daily[i][1] -= 1
                else:  # if not enough space in the remaining weekday to create a full-min shift
                    new_shift = shift(shift_id, len(daily) - min - 1, len(daily) - 1, min)
                    for i in range(len(daily) - 1 - min, len(daily) - 1):
                        daily[i][1] -= 1
                print("Created shift", new_shift.id, "Start:",new_shift.start, "End:", new_shift.end)
                result.append(new_shift)
            else:
                pos = -1
                max_ext=0
                for ts in range(len(result)):           #search for the shift with the highest extension potential
                    if result[ts].end <= index:
                        if max-result[ts].duration>max_ext:
                            max_ext = max-result[ts].duration
                            pos = ts
                print("Extended shift",result[pos].id)
                result[pos].extend(1)
                daily[index][1]-=1
                daily[index][2]-=1
        if daily[index][1] <= 0:  # if current weight is 0 or below, move index to next positive weight
            for j in range(index, len(daily)-1):
                if daily[j][1] > 0:
                    index = j
                    break
        if daily[index][1] <=0:
            index = -1

    print("Daily solution for day", weekday.dayname)
    print("Decided on",len(result),"shifts.")
    for x in range(len(result)):
        result[x].printme()
    return result



def weekly_solver(fullweek, hourly, minimum_hrs, maximum_hrs, extra=None):
    solution = schedule(fullweek)
    solution_date = fullweek.datestart
    for day in fullweek.days:
        print("Solving day",day.date)
        solution.add_shifts(daily_solver(day,hourly,minimum_hrs,maximum_hrs,extra), key=solution_date)
        solution_date +=timedelta(days=1)
    return solution


class shift:

    def __init__(self, uid, starttime, endtime, shiftduration, stype=None):
        self.id = uid                       # shift unique ID given from a higher-level class
        self.start = starttime              # shift starting time
        self.end = endtime                  # shift ending time
        self.duration = shiftduration       # shift duration in timeslots (integer)
        if stype is not None:
            self.shift_type = stype
        else:
            self.shift_type = 0

    def extend(self,timeslots, soe=1):          #extends shift, soe is (0: start, 1: end)
        self.duration += timeslots
        if soe:
            self.end += timeslots
        else:
            self.start -= timeslots

    def shorten(self,timeslots, soe=1):         #shortens shift, soe is (0: start, 1: end)
        self.duration -= timeslots
        if soe:
            self.end -= timedelta(minutes=timeslots * 15)
        else:
            self.start += timedelta(minutes=timeslots * 15)

    def printme(self):
        print("Shift",self.id," of type", self.shift_type)
        print("Start:",self.start, "  End:",self.end,"  Duration:",self.duration)



class schedule:

    def __init__(self, workweek):
        self.dayshifts = dict()        #list of day_shifts
        self.week = workweek

    def add_shifts(self,shifts,key=None):
        self.dayshifts[key] = shifts

    def printme(self,verbose=False):
        print("Schedule for ", end='')
        self.week.printme()
        if verbose:
            print("\n--------\n")
            for s in self.dayshifts:
                print("Day",s)
                for x in self.dayshifts[s]:
                    x.printme()