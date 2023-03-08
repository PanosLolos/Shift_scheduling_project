from random import seed,randint
from weekly_daily import *
from scheduler import *
from generators import *

seed(13)
# testday = daily(datetime(2022,9,28,12,0,0),datetime(2022,9,29,1,30,0))
# testday.printme()



# *********** INITIALIZE A WEEKLY SCHEDULE **************************************************************************
testweek = weekly(datetime(2022,9,28),datetime(2022,10,4))
dailies = []
weights = []
dw = []
dailies.append(
    { "start": datetime(2022,9,28,9,0,0),
      "end": datetime(2022,9,28,21,0,0)}
)
inv = get_interval_list(dailies[0]["start"],dailies[0]["end"],15)
for x in range(len(inv)):
    dw.append([x,randint(0,5)])
if len(dw)==1:
    weights.append([[0,0]])
else:
    weights.append(dw)
dw=[]
dailies.append(
    { "start": datetime(2022,9,29,9,0,0),
      "end": datetime(2022,9,29,21,0,0)}
)
inv = get_interval_list(dailies[1]["start"],dailies[1]["end"],15)
for x in range(len(inv)):
    dw.append([x,randint(0,5)])
if len(dw)==1:
    weights.append([[0,0]])
else:
    weights.append(dw)
dw=[]
dailies.append(
    { "start": datetime(2022,9,30,9,0,0),
      "end": datetime(2022,9,30,21,0,0)}
)
inv = get_interval_list(dailies[2]["start"],dailies[2]["end"],15)
for x in range(len(inv)):
    dw.append([x,randint(0,5)])
if len(dw)==1:
    weights.append([[0,0]])
else:
    weights.append(dw)
dw=[]
dailies.append(
    { "start": datetime(2022,10,1,9,0,0),
      "end": datetime(2022,10,1,17,0,0)}
)
inv = get_interval_list(dailies[3]["start"],dailies[3]["end"],15)
for x in range(len(inv)):
    dw.append([x,randint(0,5)])
if len(dw)==1:
    weights.append([[0,0]])
else:
    weights.append(dw)
dw=[]
dailies.append(
    { "start": datetime(2022,10,2,0,0,0),
      "end": datetime(2022,10,2,0,0,0)}
)
inv = get_interval_list(dailies[4]["start"],dailies[4]["end"],15)
for x in range(len(inv)):
    dw.append([x,randint(0,5)])
if len(dw)==1:
    weights.append([[0,0]])
else:
    weights.append(dw)
dw=[]
dailies.append(
    { "start": datetime(2022,10,3,9,0,0),
      "end": datetime(2022,10,3,21,0,0)}
)
inv = get_interval_list(dailies[5]["start"],dailies[5]["end"],15)
for x in range(len(inv)):
    dw.append([x,randint(0,5)])
if len(dw)==1:
    weights.append([[0,0]])
else:
    weights.append(dw)
dw=[]
dailies.append(
    { "start": datetime(2022,10,4,9,0,0),
      "end": datetime(2022,10,4,21,0,0)}
)
inv = get_interval_list(dailies[6]["start"],dailies[6]["end"],15)
for x in range(len(inv)):
    dw.append([x,randint(0,5)])
if len(dw)==1:
    weights.append([[0,0]])
else:
    weights.append(dw)
dw=[]

# *********************************************************************************************************

#testweek.build_week(dailies,weights)
# testweek.printme(1)

#day= daily_solver(testweek.days[0],4,5,8,0.12)

#
# testy = datetime(2022,10,4,9,0,0)
# print(testy)
# testy += timedelta(minutes=15)
# print(testy)
#
# tryday = daily(datetime(2022,10,4,9,0,0),datetime(2022,10,4,22,0,0))
# tryday.printme()
# weights = [[0,2],[1,2],[2,2],[3,2],
#            [4,2],[5,2],[6,2],[7,2],
#            [8,3],[9,3],[10,3],[11,3],
#            [12,3],[13,3],[14,3],[15,3],
#            [16,4],[17,4],[18,4],[19,4],
#            [20,5],[21,5],[22,5],[23,5],
#            [24,3],[25,3],[26,3],[27,3],
#            [28,2],[29,2],[30,2],[31,2],
#            [32,5],[33,5],[34,5],[35,5],
#            [36,5],[37,5],[38,5],[39,5],
#            [40,4],[41,4],[42,4],[43,4],
#            [44,4],[45,4],[46,4],[47,4],
#            [48,4],[49,4],[50,4],[51,4]]
# tryday.update_daily(weights)
# tryday.printme()
#
# tryday = generate_weighted_day(datetime(2022,10,4,9,0,0),datetime(2022,10,4,22,0,0),2,3)
# tryday.printme()
# print(tryday.get_total_workhours())
# print(tryday.get_average_weight())

#
# solution = daily_solver(tryday,4,5,8,extra=0.12)
#tryday.update_daily()
#
# tryweek = generate_weighted_week(datetime(2022,10,4,9,0,0), 2,3 )
# tryweek.printme(verbose=1)

#*************************************************************************************************
#

# myday = generate_weighted_day(datetime(2022,10,4,9,0,0),datetime(2022,10,4,22,0,0),2,3)
#
# myday.printme()

# myweek = generate_weighted_week(datetime(2022,10,4),3,4)
# myweek.printme(verbose=1)

myposts, myemps = generate_model(datetime(2022, 11, 26), 35, 2)
for i in myposts:
    i.printme()
    print(i.soft_unavailable.keys())
    print(i.available.keys())
    i.workweek.printme()
# for j in myemps:
#     j.printme()
#     j.print_schedule()




print("\n\nmoving to solver...")
for k in myposts:
    print("Solving",k.id)
    k.schedule = weekly_solver(k.workweek, 4, 5, 8, 0.12)
print("\n\n Printing solutions! \n")
for k in myposts:
    k.printme(verbose=True)
print(" DONE! ")



print("SHFT:", len(myposts[0].schedule.dayshifts[date(2022, 11, 26)]))
print("AV:  ", len(myposts[0].available))
print("SUN: ", len(myposts[0].soft_unavailable))

# print('\n\n',myposts[0].schedule.dayshifts.keys())
for k in myposts:
    k.printme()
    for g in k.schedule.dayshifts.keys():
        print(k.evaluate(0, day=g, verbose=True))



# evs = evaluate_posts_total(myposts)
# print("Total evaluations:")
# for e in evs:
#     print(e)

# print("\nDaily Evaluations:")
# print(evaluate_posts_day(myposts,date(2022,11,26)))
# print(evaluate_posts_day(myposts,date(2022,11,27)))
# print(evaluate_posts_day(myposts,date(2022,11,28)))
# print(evaluate_posts_day(myposts,date(2022,11,29)))
# print(evaluate_posts_day(myposts,date(2022,11,30)))
# print(evaluate_posts_day(myposts,date(2022,12,1)))

print("TESTS")



#
# weeklies = evaluate_posts_total(myposts)
# for w in weeklies:
#     print("Post:", w)
# rankings = [[x.id, [],[]] for x in myposts]
# rankings = get_rankings(date(2022,11,29),rankings,myposts,weeklies)
# for r in rankings:
#     print("Ranking:", r)
# chosen = choose_post(rankings)
#
# print("Chosen post:", chosen)
#
# assign(date(2022,11,27),date(2022,12,1),myemps,myposts)

# print(myposts[0].schedule.printme())
#
mytiers = generate_tiers(3)

print("* * * * * * * * * * * * * * Testing assing * * * * * * * * * * * * * *")
result = assign(date(2022,11,26),date(2022,11,27),myemps,mytiers,myposts)

#
#
# print("Current shift order")
# print("ID  DURATION START  END")
# for s in myposts[0].schedule.dayshifts[date(2022,12,1)]:
#     print(s.id, "    ", s.duration, "   ", s.start, "   ", s.end)
# print("Solving...")
# mylist = min_shifts_required(myposts[0],date(2022,11,29))
# print("Sorted shift order")
# print("ID  DURATION START  END")
# for s in mylist:
#     print(s.id, "    ", s.duration, "   ", s.start, "   ", s.end)
#

#
# print("Current shift order")
# print("ID  DURATION START  END")
# for s in myposts[0].schedule.dayshifts[date(2022,12,1)]:
#     print(s.id, "    ", s.duration, "   ", s.start, "   ", s.end)
# print("Solving...")
# mylist = sort_shifts_for_min_coverage(myposts[0],date(2022,11,26))
# print("Sorted shift order")
# print("ID  DURATION START  END")
# for s in mylist:
#     print(s.id, "    ", s.duration, "   ", s.start, "   ", s.end)


# for e in emplist:
#     e[1]['Total_min'] = e[1]['min_hours'] * e[1]['min_shifts']  # leftover hours*shifts will be used for equalizing pay
#     e[1]['Total_max'] = e[1]['max_hours'] * e[1]['max_shifts']

# print("Testing for skeleton crew min coverage")
# myposts[0].workweek.printme()
#
# myposts[0].schedule.printme(verbose=True)
#
#





# myshifts = min_shifts_required(myposts[0], date(2022, 11, 27))
# for m in myshifts:
#     m.printme()

# solution = weekly_solver(myposts[0].workweek,4,5,8,0.12)
# solution.printme(verbose=True)
# #
# myposts[0].get_employees(myemps,2)
# #
# td = datetime(2022,11,25)
# print(td)
# td = td+timedelta(days=1)
# print(td.date())


# emps = generate_random_employees(10,3,2)

# start_date = datetime(2022,11,26)
# end_date = start_date + timedelta(days=7)
# print("start:",start_date,"  end:",end_date)
# print("nstart:",start_date.strftime('%d/%m/%Y'),'    nend:',end_date.strftime('%d/%m/%Y'))

