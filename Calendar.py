#!/usr/bin/env python
# coding: utf-8

# In[16]:


import calendar
import matplotlib.pyplot as plt
import numpy as np


# In[17]:
    

days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
months = ['','January','February','March','April','May','June','July','August','September','October','November','December']

# This is a good use case for enums.  Look up python Enums and see how they are used.  
# from enum import Enum

# class Months(Enum)
#   JANUARY = 0
#   FEBRUARY = 1
#   ...

# class Days(Enum)
#     SUNDAY = 0
#     MONDAY = 1
#     ...

calendar.setfirstweekday(6)

class MyCalendar():
    
    # Python3 allows type hints.  Type hints are very useful for understanding data structures.  
    def __init__(self, year: int, month: int): 
        # initiate calendar with years
        self.year = year
        self.month = month
        self.cal = calendar.monthcalendar(year,month)
        
        # store events in the calendar in same format as calendar
        self.events = [[[] for day in week] for week in self.cal]
    
    def index_monthday(self,day):
        # index the day in the list of lists
        for week_n, week in enumerate(self.cal):
            try:
                return week_n, week.index(day)
            except ValueError:
                pass
        raise ValueError('There are not {} days in this month'.format(day))
        
    def add_event(self, day, event_str):
        # add event to the calendar
        week, w_day = self.index_monthday(day)
        self.events[week][w_day].append(event_str)
    
    # I assume this makes a visualization in the jupyter notebook?  Very cool.  You can embed this 
    # jupyter notebook into your personal website actually.  Look up saving the notebook as html.
    # It won't be interactive but they will be able to see the calendar.  
    def show(self):
        #display the calendar
        f, axs = plt.subplots(len(self.cal), 7, sharex = True, sharey = True, figsize = (20,15))
        for week, row in enumerate(axs):
            for week_day, ax in enumerate(row):
                ax.set_xticks([])
                ax.set_yticks([])
                if self.cal[week][week_day] != 0:
                    ax.text(0.02, 0.98, str(self.cal[week][week_day]),va = 'top', ha = 'left')
                events = "\n".join(self.events[week][week_day])
                ax.text(0.03, 0.85, events,va = 'top', ha = 'left', fontsize = 10)
        
        for n, day in enumerate(days):
            axs[0][n].set_title(day, fontsize = 10)
        
        f.subplots_adjust(hspace=0)
        f.subplots_adjust(wspace=0)
        
        f.suptitle(months[self.month] + ' ' + str(self.year),fontsize=20, fontweight='bold')
        
        plt.show()


# In[23]:


# create the calendar for use
yearcalendar = []

year = int(input('What year would you like to use for your calendar? '))

for x in range(1,13):
    cal = MyCalendar(year, x)
    yearcalendar.append(cal)

active = True

# functions for actions to perform on the calculator 
# schedule events in the calendar


# long functions are hard to understand.  When a function gets long it is good to break out some of the logic into other functions.  Think about the 
# different cases this function is handling and see if you can move some of the code in here into functions that handle each specific case.  There
# is nothing wrong with small functions.  Great code often reads like pseudo codem or a list of instructions.  A function can call several other 
# functions that abstract away the complexity.  

def schedule(yearcalendar):
    scheduling = True

    while scheduling:
        recur = input('Would you like to schedule this as a recurring event (y or n)? ')

        month = int(input('What month would you like to schedule an event for? '))

        if recur == 'n':
            day = int(input('What day would you like to schedule and event for? '))
            
        is_time = input('Would you like to add a time to your event (y or n)? ')

        event = input('What is the event? ')

        # schedule timed events
        if is_time == 'y':
            time = input('What time is the event? ')
            # schedule recurring timed events
            if recur == 'y':
                freq = input('Would you like to schedule this event daily(enter d) or weekly(enter w)? ')
                if freq == 'd':
                    for week in yearcalendar[month-1].cal:
                        for day in week:
                            if day == 0:
                                pass
                            else:
                                yearcalendar[month - 1].add_event(day, event + ' @ ' + time) 
                elif freq == 'w':
                    fweek = ['s','m','t','w','th','f','sa']
                    fday = input('What day of the week would you like to schedule this event for(su,m,t,w,th,f,sa)?')
                    numday = fweek.index(fday)
                    for week in yearcalendar[month-1].cal:
                        if week[numday] == 0:
                            pass
                        else:
                            yearcalendar[month - 1].add_event(week[numday], event + ' @ ' + time)
            else:
                yearcalendar[month - 1].add_event(day, event + ' @ ' + time)
       
        # schedule untimed events       
        else:
            # schedule recurring untimed events
            if recur == 'y':
                freq = input('Would you like to schedule this event daily(enter d) or weekly(enter w)? ')
                if freq == 'd':
                    for week in yearcalendar[month-1].cal:
                        for day in week:
                            if day == 0:
                                pass
                            else:
                                yearcalendar[month - 1].add_event(day, event)  
                elif freq == 'w':
                    # This code is very similar to the code above.  See if you can generalize it and use a function that you can call 
                    # in both places.  
                    fweek = ['s','m','t','w','th','f','sa']
                    fday = input('What day of the week would you like to schedule this event for(su,m,t,w,th,f,sa)? ')
                    numday = fweek.index(fday)
                    for week in yearcalendar[month-1].cal:
                        if week[numday] == 0:
                            pass
                        else:
                            yearcalendar[month - 1].add_event(week[numday], event)

            else:   
                yearcalendar[month - 1].add_event(day, event)

        cont_sched = input('Would you like to continue scheduling (y or n)? ')

        if cont_sched == 'n':
            scheduling = False
        else:
            pass

# search for events in the calendar
def search(yearcalendar):
    searching = True
    
    while searching:
        
        found = False
        
        search_is_time = input('Is there a time associated with the event that your are searching for (y or n)? ')
        
        recur_search = input('Are you searching for a recurring event (y or n)?')
    
        searchevent = input('What event would you like to search for? ')
        
        if search_is_time == 'y':
            stime = input('What time is the event? ')
            searchevent = searchevent + ' @ ' + stime
        
        #search for recurring events
        if recur_search == 'y':
            freq = input('At what frequency does this event occur? Enter d(daily) or w(weekly) ')
            if freq == 'd':
                for calend in yearcalendar:
                    for week in calend.events:
                        for event in week:
                            if searchevent == ''.join(event):
                                found = True
                                dmonth = calend.month
                if found:
                    print('Event Found everyday in ' + months[dmonth])
                elif not found:
                     print('Could not find event in calendar')
            elif freq == 'w':
                for calend in yearcalendar:
                    for week in calend.events:
                        for event in week:
                            if searchevent == ''.join(event):
                                found = True
                                dmonth = calend.month
                if found:
                    print('Event Found weekly in ' + months[dmonth])
                elif not found:
                     print('Could not find event in calendar')
                
                                
        #search for the events 
        else:
            for calend in yearcalendar:
                for week in calend.events:
                    weeknum = calend.events.index(week)
                    for event in week:
                        daynum = week.index(event)
                        if searchevent == ''.join(event):
                            found = True
                            print('Event Found on ' + months[calend.month] + ' ' + str(calend.cal[weeknum][daynum]))

            if not found:
                print('Could not find event in calendar') 
        
        cont_sear = input('Would you like to continue searching (y or n)? ')
    
        if cont_sear == 'n':
            searching = False
        else:
            pass

# browse the calendar
def browse(yearcalendar):
    for cal in yearcalendar:
        cal.show()

# run logic for calendar
while active:
    action = input('What would you like to do with your calender? Enter s for schedule, se for search, or b for browse ')

    if action == 's':
        schedule(yearcalendar)
    elif action == 'se':
        search(yearcalendar)
    elif action == 'b':
        browse(yearcalendar)
    
    cont_act = input('Would you like to perform another action on your calendar (y or n)? ')
    
    if cont_act == 'n':
        active = False
    else:
        pass

