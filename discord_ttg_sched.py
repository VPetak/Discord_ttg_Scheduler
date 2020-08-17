import discord
import pickle
from discord.ext import commands

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
DEBUG_OFFLINEMODE = False

## TO DO LIST ## ------------------------------------------------------------------------------------------------------------------------------------------------

# if user already voted Monday 1pm-3pm, and vote later for Monday 2pm-10pm, the latest entry should override previous entries for the same day

# add something to automatically close the poll at a specified time, currently user must use the "!close" command

# add ability to make it so only a certain role can vote, such as a "players" role

    # optional feature to message people who haven't voted yet to remind them

# look into cogs (currently regular classes are used)

# see if there's a way for python to interpret time in a way consistant with how users would enter it in the command that also works with intervals (minutes don't matter since it's meant to give the DM a general idea of when to begin)

# Maybe change how the optimal time is chosen, if only one person is arriving much later than everyone else (as is often the case), their 1 vote would currently make the game start very late, even if everyone else can make it earlier

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
# START

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# OBJECTS
class pollobj: #this is meant to replace poll, polltime, and voterlist by putting all that info in one object containing the number of votes for a given day, optimal times, and a list of voters
    #the name of the day will be stored in a dictionary
    def __init__(self):
        self.name = ""
        self.votes = 0
        self.tstart = 6
        self.tend = 24
        self.voters = [] #could use length of voters list as the # of votes. Get some easy uniqueness to voters by using a set. If you have a set and add kevin twice, you only have one instance. A set is a dict with no associated values.
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# BALLOT (these handle the data directly, and are called by the commands)

class Ballot():
    def __init__(self):
        # each int represents an hour of the day, 0 is midnight. Although 0-6 technically would be the next day on the calendar,
        # for the purposes of this 0-6 will count as the same day, so a session can go from Monday 8pm-2am without making things confusing
        # only need for this is to track how late people want to be up, and how late the DM should expect players to be on
        self.ballotbox = {} #will contain the voteobj's, replacing the need for voterlist, poll, and polltime
        # self.timetuple is used later to convert these strings to their 24hr clock equivalents. Half-hours are not supported but will probably be added later
        self.timetuple = (("12am", 0), ("12:30am", 0),("midnight", 0), ("mdnt", 0), ("-1am", "-1"), ("1am-", "1-"), ("1:30am", 1), ("-2am", "-2"), ("2am-", "2-"), ("2:30am", 2), ("3am", 3), ("3:30am", 3), ("4am", 4), ("4:30am", 4), ("5am", 5), ("5:30am", 5), ("6am", 6), ("6:30am", 6),
                     ("7am", 7),("7:30am", 7), ("8am", 8), ("8:30am", 8), ("9am", 9), ("9:30am", 9), ("10am", 10), ("10:30am", 10), ("11am", 11), ("11:30am", 11), ("12pm", 12), ("12:30pm", 12), ("noon", 12),
                     ("-1pm", "-13"), ("1pm-", "13-"), ("1:30pm", 13), ("-2pm", "-14"), ("2pm-", "14-"), ("2:30pm", 14), ("3pm", 15), ("3:30pm", 15), ("4pm", 16), ("4:30pm", 16), ("5pm", 17), ("5:30pm", 17), ("6pm", 18), ("6:30pm", 18), ("7pm", 19), ("7:30pm", 19),
                     ("8pm", 20), ("8:30pm", 20), ("9pm", 21), ("9:30pm", 21), ("10pm", 22), ("10:30pm", 22), ("11pm", 23), ("11:30pm", 23))
        self.sched_up = False


    def assign(self): #this function will be called at a certain time (determined by an automatic deadline command) or a manual command
        if self.sched_up == False:
            return str("No schedule to assess")
        sortedballotkeys = sorted(self.ballotbox, key=lambda x: self.ballotbox[x].votes, reverse=True)
        retstr = "Optimal times:\n-------------\n"
        stopat = 3 #how many entries should we return here. Setting this to 3 shows the top 3, 10 would be top 10, 1 would only show the best, and so on
        for key in sortedballotkeys:
            if stopat <= 0:
                break
            if key == "" or self.ballotbox[key].votes == 0:
                continue
            else:
                retstr += key + "\n" + f"from  {self.ballotbox[key].tstart} to {self.ballotbox[key].tend}" + "\n Participants for this day: "
                for voter in self.ballotbox[key].voters:
                    retstr += f"{voter} "
                stopat -= 1
        self.sched_up = False
        return retstr

    
    def schedule(self, args):
        retStr = ''
        for i in args:
            retStr = retStr + "\n" + i
            self.ballotbox[i] = pollobj() #make a new pollobj for each day scheduled as a possible date
            self.ballotbox[i].name = i
        self.sched_up = True
        return("Vote on the following days:\n\n\n" + retStr.replace("_", " ") + "\n--------------\nExample: !vote A 5pm-11pm")

    
    def castvote(self, arg, time, author):
        print("vote: " + arg + " " + time)
        global DEBUG_MULTIVOTE
        arg = arg.upper()
        time = time.lower()

        if self.sched_up == False:
            return("Sorry! There's no schedule to vote on!")
        elif arg not in self.ballotbox:
            return("Invalid vote: " + arg + " :no_smoking:")
        elif time == None: 
            return( "Please specify a time range in 24hr format, ex\n!vote A 19-1\n This would vote for whatever day A represents from 7pm to 1am") 
        else:
            
            #check if this person already voted
            if author in self.ballotbox[arg].voters and DEBUG_MULTIVOTE == False:
                return("You may only vote once for a given day in the poll, however you are encouraged to vote for multiple days if your schedule allows it.")

            # first convert the time to a 24hr format, also catches noon and midnight for easier use
            if "m" in time or "n" in time: #check if am/pm format, if not there's no point in doing the conversion. Noon and Midnight or abbreviated mdnt are covered since it looks for m and n
                for t in range(0, len(self.timetuple)):
                    time = time.replace(self.timetuple[t][0], str(self.timetuple[t][1]))
            
            self.ballotbox[arg].votes += 1 #increment the day's poll first
            print("time: " + time)

            self.ballotbox[arg].voters.append(author) #Log the voter in a list of voters
            
            timerange = time.split("-") #split the time range into two values in an array with 2 indices, check if it spills over past 12 midnight
            past12 = False
            print("timerange[0-1]: " + timerange[0] + " - " + timerange[1])
            timerangeint = [int(i) for i in timerange]
            
            if int(timerangeint[0]) > int(timerangeint[1]) or int(timerangeint[0]) in range(0,6):
                past12 = True
                print("past12: TRUE")
            
            if past12 == False:
                if timerangeint[0] > self.ballotbox[arg].tstart:
                    self.ballotbox[arg].tstart = timerangeint[0]
                if timerangeint[1] < self.ballotbox[arg].tend:
                    self.ballotbox[arg].tend = timerangeint[1]
            else:
                if timerangeint[0] > self.ballotbox[arg].tstart or (timerangeint[0] >= 0 and timerangeint[0] < 6 and (self.ballotbox[arg].tstart in range(6, 24))):
                    #this if statement is long, but it checks to see if start time is past midnight and modifies tstart accordingly REVIEW THIS LATER
                    self.ballotbox[arg].tstart = timerangeint[0]
                if timerangeint[1] < self.ballotbox[arg].tend or timerangeint[1] in range(6, 24):
                    self.ballotbox[arg].tend = timerange[1]
            
            return("Your vote for " + arg + " has been cast\n Thanks for voting, " + str(author) + "!")
    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# COMMANDS (these should call ballot functions rather than handling the data directly)

#class Cmds(commands.Cog):
class Cmds():

    @bot.command()
    async def close(ctx):
        result = ballot.assign()
        await ctx.send(result)

    @bot.command()
    async def sched(ctx, *args):
        if len(args) < 1:
            await ctx.send("Please enter the possible times you want to schedule separated by spaces (Use _ for spaces like 'Monday_4/20_4:20PM)")
        else:
            ballot.__init__() #create an instance of the Ballot class
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

    print(testballot.schedule(["A", "B", "C"]))
    
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
