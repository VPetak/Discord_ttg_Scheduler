import discord
import pickle
from discord.ext import commands

#the line above and below both have similar functions, see here https://stackoverflow.com/questions/53980371/discord-bot-does-not-respond-to-commands
bot = commands.Bot(command_prefix='!')

token = pickle.load(open("token.p", "rb"))
# ^ have a binary file encoded using pickle in the same directory in order for this to work.
# If you modify this just make sure it receives the token in string form somehow, as it is unwise to have it in plaintext here

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
# DEBUG VARIABLES
# Use these global finals for testing, all of them should be set to False, and none of them should be modified later in the code

# Determines whether the same person can vote more than once
DEBUG_MULTIVOTE = False

# Runs the code without using commands or putting the bot online
DEBUG_OFFLINEMODE = True

## TO DO LIST ## ------------------------------------------------------------------------------------------------------------------------------------------------

# make it so each person can only vote on a specified time once

    # if they already voted Monday 1pm-3pm, and vote later for Monday 2pm-10pm, the latest entry should override previous entries for the same day

# add something to automatically close the poll at a specified time, currently user must use the "!close" command

# add ability to make it so only a certain role can vote, such as a "players" role

    # optional feature to message people who haven't voted yet to remind them

# look into cogs (currently regular classes are used)

# look into the possibility of using a dictionary instead of a list for the self.poll, there might be a more efficient way to process the self.poll

# see if there's a way for python to interpret time in a way consistant with how users would enter it in the command that also works with intervals (minutes don't matter since it's meant to give the DM a general idea of when to begin)

# Maybe change how the optimal time is chosen, if only one person is arriving much later than everyone else (as is often the case), their 1 vote would currently make the game start very late, even if everyone else can make it earlier

# some things (like the nested lists in self.poll) might be better off as objects

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
# START

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# OBJECTS

class voteobj(object): #this object class logs details of every vote cast
    def __init__(self, name, day, time):
        self.name = name
        self.day = int(day)
        self.time = str(time)
    def __str__(self):
        retString = str(self.name) + ": day" + str(self.day) + " time" + self.time
        return retString

class resultobj(object): #this object class is used by the assign() method and stores best day, start of optimal time range, and end of optimal time range
    def __init__(self, day, tstart, tend):
        self.day = int(day)
        self.tstart = tstart
        self.tend = tend
    def __str__(self):
        retString = str(self.name) + ": day" + str(self.day) + " time" + self.time
        return retString
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# BALLOT (these handle the data directly, and are called by the commands)

class Ballot():
    def __init__(self):
        # each of these represents an hour of the day, 0 is midnight. Although 0-6 technically would be the next day on the calendar,
        # for the purposes of this 0-6 will count as the same day, so a session can go from Monday 8pm-2am without making things confusing
        # only need for this is to track how late people want to be up, and how late the DM should expect players to be on
        self.poll = [['A', -1, 0], ['B', -1, 1], ['C', -1, 2], ['D', -1, 3], ['E', -1, 4], ['F', -1, 5], ['G', -1, 6], ['H', -1, 7], ['I', -1, 8], ['J', -1, 9], ['K', -1, 10], ['L', -1, 11], ['M', -1, 12], ['N', -1, 13]]#[day name, votes, index]
        #redo as an object?

        self.voterlist = [[], [], [], [], [], [], [], [], [], [], [], [], [], []] # a list of lists, each for corresponds to a day, tracks who voted for which day to avoid double votes and let people correct their votes. Type = voteobj object
        # self.polltime is a list of every hour for every day, used to determine a suggested start and end time
        self.polltime = []
        for i in range(0, len(self.poll)):
            self.polltime.append([[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
                    [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]])

        # self.timetuple is used later to convert these strings to their 24hr clock equivalents. Half-hours are not supported but will probably be added later
        self.timetuple = (("12am", 0), ("12:30am", 0),("midnight", 0), ("mdnt", 0), ("-1am", "-1"), ("1am-", "1-"), ("1:30am", 1), ("-2am", "-2"), ("2am-", "2-"), ("2:30am", 2), ("3am", 3), ("3:30am", 3), ("4am", 4), ("4:30am", 4), ("5am", 5), ("5:30am", 5), ("6am", 6), ("6:30am", 6),
                     ("7am", 7),("7:30am", 7), ("8am", 8), ("8:30am", 8), ("9am", 9), ("9:30am", 9), ("10am", 10), ("10:30am", 10), ("11am", 11), ("11:30am", 11), ("12pm", 12), ("12:30pm", 12), ("noon", 12),
                     ("-1pm", "-13"), ("1pm-", "13-"), ("1:30pm", 13), ("-2pm", "-14"), ("2pm-", "14-"), ("2:30pm", 14), ("3pm", 15), ("3:30pm", 15), ("4pm", 16), ("4:30pm", 16), ("5pm", 17), ("5:30pm", 17), ("6pm", 18), ("6:30pm", 18), ("7pm", 19), ("7:30pm", 19),
                     ("8pm", 20), ("8:30pm", 20), ("9pm", 21), ("9:30pm", 21), ("10pm", 22), ("10:30pm", 22), ("11pm", 23), ("11:30pm", 23))

        self.sched_up = False



    def showPoll(self):
        ret_str = ""
        #global self.poll
        #global self.polltime
        for i in range(0, len(poll)): #len(poll) was 14 originally, but I changed it just in case I increase the maximum number of days to vote on
            if self.poll[i][1] == -1:
                return ret_str
            elif self.poll[i][1] == 0:
                ret_str = ret_str + "\n-------------------------\n" + self.poll[i][0] + ": no votes"
            else:
                ret_str = ret_str + "\n-------------------------\n" + str(self.poll[i][0]) + ": " + str(self.poll[i][1]) + "\nTime:\n"
                for j in range(0,len(self.polltime)): #len(polltime was 23 previously, but doing this should be less work when I add 30 min intervals
                    if self.polltime[i][j][0] < 1:
                        continue
                    else:
                        ret_str = ret_str + str(self.polltime[i][j][1]) + " " + str(self.polltime[i][j][0]) + "  "
        return ret_str



    def assign(self): #this function will be called at a certain time (determined by an automatic deadline command) or a manual command
        #global self.poll
        #global self.polltime
        #global self.sched_up
        #global self.voterlist
        if self.sched_up == False:
            return str("No schedule to assess")

        polls = self.poll.copy() #making a copy since the original setup requires self.poll to be in its original order when finding the optimal time ranges

        no = [resultobj(0, 7, -1), resultobj(-1, 7, -1), resultobj(-1, 7, -1)] # A list of the top 3, no[0] is for number one and so on. Remember resultobj's contain "day", time start ("tstart"), and time end ("tend")

        #simpler way to get top 3:  store the original index in the self.poll array at index [i][2], then sort it and get those indices from the last 3 in reverse order (as the one with the most votes will be last)
        polls.sort(key = lambda x: x[1])

        no[0].day = polls[len(polls)-1][2]
        no[1].day = polls[len(polls)-2][2]
        no[2].day = polls[len(polls)-3][2]


        for d in range(0, 3):
            for i in range(7, 24): #find the best time range, before midnight 
                if self.polltime[no[d].day][i][0] > self.polltime[no[d].day][no[d].tstart][0]: #logic for best start time, check if this next hour has more votes than the previous best
                    no[d].tstart = i
                else:
                    continue
            for i in range(0, 7): #logic for midnight to 6 start time votes, but seriously who would start this late?
                if self.polltime[no[d].day][i][0] > self.polltime[no[d].day][no[d].tstart][0]: 
                    no[d].tstart = i
                else:
                    continue
            no[d].tend = no[d].tstart # prevent the next loop from checking before the start point, since it's impossible to end before the start time, and it would be a waste of time to check
            for i in range(no[d].tstart, 24): #find the best end time , before midnight
                if self.polltime[no[d].day][i][0] < self.polltime[no[d].day][no[d].tend][0]: #logic for best end time, check to see if the next hour is lower and sets the endpoint there
                    no[d].tend = i
                    break
                else:
                    continue
            for i in range(0, 7): #find the best end time, from midnight to 6, as these things often go past midnight. For the purposes of this bot, it will be counted as the same day in the self.poll
                if self.polltime[no[d].day][i][0] < self.polltime[no[d].day][no[d].tend][0]: #logic for best end time, check to see if the next hour is lower and sets the endpoint there
                    no[d].tend = i
                    break
                else:
                    continue
            
        retstr = "Optimal times:\n-------------\n" + self.poll[no[0].day][0] + "\nfrom " + self.polltime[no[0].day][no[0].tstart][1] + " to " + self.polltime[no[0].day][no[0].tend][1] + "\n Participants for this day: "
        for i in range(0, len(self.voterlist[no[0].day])):
            retstr = retstr + str(self.voterlist[no[0].day][i].name) + " "

        if no[1].day != -1:
            retstr = retstr + "\n-------------\n" + self.poll[no[1].day][0] + "\nfrom " + self.polltime[no[1].day][no[1].tstart][1] + " to " + self.polltime[no[1].day][no[1].tend][1] + "\n Participants for this day: "
            for i in range(0, len(self.voterlist[no[1].day])):
                retstr = retstr + str(self.voterlist[no[1].day][i].name) + " "

        if no[2].day != -1:
            retstr = retstr + "\n-------------\n" + self.poll[no[2].day][0] + "\nfrom " + self.polltime[no[2].day][no[2].tstart][1] + " to " + self.polltime[no[2].day][no[2].tend][1] + "\n Participants for this day: "
            for i in range(0, len(self.voterlist[no[2].day])):
                retstr = retstr + str(self.voterlist[no[2].day][i].name) + " "
        self.sched_up = False
        return retstr

    
    def schedule(self, args):
        #global self.sched_up
        #global self.poll
        retStr = ''
        for i in range(0, len(args)):
            retStr = retStr + "\n" + self.poll[i][0] + " " + args[i]
            self.poll[i][1] = 0
            self.poll[i][0] = args[i] #save the string of the day to be voted on
        self.sched_up = True
        return("Vote on the following days:\n\n\n" + retStr.replace("_", " ") + "\n--------------\nExample: !vote A 5pm-11pm")

    
    def castvote(self, arg, time, author):
        print("vote: " + arg + " " + time)
        #global self.sched_up
        #global self.poll
        #global self.polltime
        #global self.voterlist
        #global self.timetuple
        global DEBUG_MULTIVOTE
        arg = arg.upper()
        time = time.lower()
        if arg == 'A':
            day = 0
        elif arg == 'B':
            day = 1
        elif arg == 'C':
            day = 2
        elif arg == 'D':
            day = 3
        elif arg == 'E':
            day = 4
        elif arg == 'F':
            day = 5
        elif arg == 'G':
            day = 6
        elif arg == 'H':
            day = 7
        elif arg == 'I':
            day = 8
        elif arg == 'J':
            day = 9
        elif arg == 'K':
            day = 10
        elif arg == 'L':
            day = 11
        elif arg == 'M':
            day = 12
        elif arg == 'N':
            day = 13
        else:
            day = -1

        if self.sched_up == False:
            return("Sorry! There's no schedule to vote on!")
        elif day == -1 or self.poll[day][1] == -1:
            return("Invalid vote: " + arg + " :no_smoking:")
        elif time == None: 
            return( "Please specify a time range in 24hr format, ex\n!vote A 19-1\n This would vote for whatever day A represents from 7pm to 1am") 
        else:

            #check if this person already voted
            if str(author) in self.voterlist and DEBUG_MULTIVOTE == False:
                return("You may only vote once, " + str(author))
            
            # first convert the time to a 24hr format, also catches noon and midnight for easier use
            if "m" in time or "n" in time: #check if am/pm format, if not there's no point in doing the conversion. Noon and Midnight or abbreviated mdnt are covered since it looks for m and n
                for t in range(0, len(self.timetuple)):
                    time = time.replace(self.timetuple[t][0], str(self.timetuple[t][1]))
            
            self.poll[day][1] = self.poll[day][1] + 1 #increment the day's poll first
            print("time: " + time)

            self.voterlist[day].append(voteobj(author, day, time)) #log this vote into our list for later use
            
            timerange = time.split("-") #split the time range into two values in an array with 2 indices, check if it spills over past 12 midnight
            past12 = False
            print("timerange[0-1]: " + timerange[0] + " - " + timerange[1])
            if int(timerange[0]) > int(timerange[1]):
                past12 = True
                print("past12: TRUE")
            if past12 == False:
                for i in range(int(timerange[0]), int(timerange[1])): #if the range doesn't go past 12, simply vote for every hour in this range
                    if self.polltime[day][i][0] == -1:
                        self.polltime[day][i][0] = 0
                    self.polltime[day][i][0] += 1
            else:
                for i in range(int(timerange[0]), 24): #otherwise we have to give it a range for the time before 12 and another for after
                    if self.polltime[day][i][0] == -1:
                        self.polltime[day][i][0] = 0
                    self.polltime[day][i][0] = self.polltime[day][i][0] + 1
                for i in range(0, int(timerange[1])): 
                    if self.polltime[day][i][0] == -1: 
                        self.polltime[day][i][0] = 0
                    self.polltime[day][i][0] = self.polltime[day][i][0] + 1 
            return("Your vote for " + arg + " has been cast\n Thanks for voting, " + str(author) + "!")
    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# COMMANDS (these should call ballot functions rather than handling the data directly)

#class Cmds(commands.Cog):
class Cmds():
    
    @bot.command()
    async def close(ctx):
        #global self.sched_up
        result = ballot.assign()
        #self.sched_up = False
        await ctx.send(result)

    @bot.command()
    async def sched(ctx, *args):
        if len(args) < 1:
            await ctx.send("Please enter the possible times you want to schedule separated by spaces (Use _ for spaces like 'Monday_4/20_4:20PM)")
        else:
            #ballot = Ballot() #create an instance of the Ballot class     this line causes Sched up to always be false. Look into later, probably has to do with scope
            # TO DO: When an old ballot is used, it's data persists, so make sure to sanitize the data when the ballot is closed
            await ctx.send(ballot.schedule(args))

    @bot.command()
    async def vote(ctx, arg, time):
        await ctx.send(ballot.castvote(arg, time, ctx.author))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# DEBUG OFFLINE TEST
# Test logic for the Ballot class by writing code in the if statement. DEBUG_OFFLINEMODE must be False.
# This is in place of commands, so make the code mimic what typical users would do
if DEBUG_OFFLINEMODE == True:
    print("DEBUG: OFFLINE TEST")
    testballot = Ballot()

    print(testballot.schedule(["#1", "#2", "#3"]))
    
    print(testballot.castvote("A", "2pm-3pm", "username"))
    print(testballot.castvote("A", "2pm-3pm", "username2"))
    print(testballot.castvote("A", "2pm-3pm", "otheruser"))
    print(testballot.castvote("A", "2pm-3pm", "username"))

    print(testballot.assign())

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------  

if DEBUG_MULTIVOTE == True:
    print("DEBUG: MULTIVOTE ENABLED!\nPLEASE DISABLE MULTIVOTE OR USERS WILL BE ABLE TO VOTE MORE THAN ONCE")
if DEBUG_OFFLINEMODE == False:
    ballot = Ballot() #create an instance of the Ballot class

    #bot.add_cog(Cmds())
    bot.run(token) #should probably be the very last thing that happens in the code
