import discord
from discord.ext import commands

#client = discord.Client()
#the line above and below both have similar functions, see here https://stackoverflow.com/questions/53980371/discord-bot-does-not-respond-to-commands
bot = commands.Bot(command_prefix='!')
token = 'PLACEHOLDER, REPLACE THIS TEXT WITH YOUR CLIENT TOKEN'
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


sched_up = False #use this to see if there's an active schedule
                                            

poll = [['A', -1], ['B', -1], ['C', -1], ['D', -1], ['E', -1], ['F', -1], ['G', -1], ['H', -1], ['I', -1], ['J', -1], ['K', -1], ['L', -1], ['M', -1], ['N', -1]]

polltime = [[[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]],
            [[-1, "mdnt"], [-1, "1am"], [-1, "2am"], [-1, "3am"], [-1, "4am"], [-1, "5am"], [-1, "6am"], [-1, "7am"], [-1, "8am"], [-1, "9am"], [-1, "10am"],
            [-1, "11am"], [-1, "noon"], [-1, "1pm"], [-1, "2pm"], [-1, "3pm"], [-1, "4pm"], [-1, "5pm"], [-1, "6pm"], [-1, "7pm"], [-1, "8pm"], [-1, "9pm"], [-1, "10pm"], [-1, "11pm"]]]

# each of these represents an hour of the day, 0 is midnight. Although 0-6 technically would be the next day on the calendar,
# for the purposes of this 0-6 will count as the same day, so a session can go from Monday 8pm-2am without making things confusing
# only need for this is to track how late people want to be up, and how late the DM should expect players to be on

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

##    if message.content.startswith('$hello'):
##        await message.channel.send('Hello!')

##    if message.content.startswith('!schedule'):
##        await message.channel.send('Hello!')

def showPoll():
    ret_str = ""
    global poll
    global polltime
    for i in range(0, 14):
        if poll[i][1] == -1:
            return ret_str
        elif poll[i][1] == 0:
            ret_str = ret_str + "\n-------------------------\n" + poll[i][0] + ": no votes"
        else:
            ret_str = ret_str + "\n-------------------------\n" + str(poll[i][0]) + ": " + str(poll[i][1]) + "\nTime:\n"
            for j in range(0,23):
                if polltime[i][j][0] < 1:
                    continue
                else:
                    ret_str = ret_str + str(j) + " " + str(polltime[i][j][1]) + "  "
    return ret_str


@bot.command()
async def foo(ctx):
    await ctx.send('bar')

@bot.command()
async def hello(ctx, arg):
    if arg == 'gordon':
        await ctx.send('HELLO ' + arg.upper() + '!')
    else:
        await ctx.send('hello ' + arg)

@bot.command()
async def sched(ctx, *args):
    global sched_up
    global poll
    if len(args) < 1:
        await ctx.send("Please enter the possible times you want to schedule separated by spaces (Use _ for spaces like 'Monday_4/20_4:20PM)")
        sched_up = False #for testing, remove later
    else:
        retStr = ''
        for i in range(0, len(args)):
            retStr = retStr + "\n" + poll[i][0] + " " + args[i]
            poll[i][1] = 0
            poll[i][0] = args[i] #save the string of the day to be voted on
        sched_up = True
        await ctx.send("Vote on the following days:\n\n\n" + retStr.replace("_", " "))

@bot.command()
async def vote(ctx, arg, time):
    global sched_up
    global poll
    global polltime
    arg = arg.upper()
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

    #check for am or pm

    if sched_up == False:
        await ctx.send("Sorry! There's no schedule to vote on!")
    elif day == -1 or poll[day][1] == -1:
        await ctx.send("Invalid vote: " + arg + " :no_smoking:")
    elif time == None:
        await ctx.send("Please specify a time range in 24hr format, ex\n!vote A 19-1\n This would vote for whatever day A represents from 7pm to 1am") 
    else:
        poll[day][1] = poll[day][1] + 1 #figure out how to replace the 0 with something that will find the right letter
        timerange = time.split("-") #split the time range into two values in an array with 2 indices, check if it spills over past 12 midnight
        past12 = False
        if timerange[0] > timerange[1]:
            past12 = True
        if past12 == False:
            for i in range(int(timerange[0]), int(timerange[1])): #if the range doesn't go past 12, simply vote for every hour in this range
                if polltime[day][i][0] == -1:
                    polltime[day][i][0] = 0
                polltime[day][i][0] += 1
        else:
            for i in range(int(timerange[0]), 24): #otherwise we have to give it a range for the time before 12 and another for after
                if polltime[day][i][0] == -1:
                    polltime[day][i][0] = 0
                polltime[day][i][0] = polltime[day][i][0] + 1
            for i in range(0, int(timerange[1])):
                if polltime[day][i][0] == -1:
                    polltime[day][i][0] = 0
                polltime[day][i][0] = polltime[day][i][0] + 1 
        await ctx.send("Your vote for " + arg + " has been cast\n" + showPoll())

        

#client.run(token)
#see comment above about the client and bot (the one with the stack overflow link
bot.run(token)



