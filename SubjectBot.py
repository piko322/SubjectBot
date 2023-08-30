#Class Reminder + link
#Possible assignment reminder
import math, discord, asyncio
from discord.ext import commands, tasks
from itertools import cycle
from time import gmtime, localtime, strftime, ctime
from random import randint as randint
#I removed my bot token for obvious reasons
TOKEN = ******
prefix = '$'
client = commands.Bot(command_prefix=prefix)
reminderOn = 1
internalreminderOn = True
reminder_states = ['','enabled.','disabled.']

#Make changes to these variables
linkDict = {'Indo Studies':'https://meet.google.com/txh-kxsw-zbu','Indonesian B':'https://meet.google.com/txh-kxsw-zbu', 'Civics':'https://meet.google.com/oyy-pxjx-mnq', 'Indonesian A':'https://meet.google.com/oyy-pxjx-mnq', 'ESS':'https://meet.google.com/yyx-ymzm-bda', 'Physics':'https://meet.google.com/eja-kcsa-hoo?pli=1&authuser=1', 'Chemistry':'https://meet.google.com/eor-oopz-ynm', 'Maths AI SL':'', 'English LL':'https://meet.google.com/tar-ejth-cfg', 'Business Management':'https://meet.google.com/uws-vyjp-ubz', 'Economics':'https://meet.google.com/dqa-osie-vwt', 'Computer Science': 'https://meet.google.com/mkg-oimj-qvc', 'Chinese B': 'https://meet.google.com/pdw-otdq-zju?authuser=0', 'Maths AA SL':'https://meet.google.com/bru-irpc-rdx','TOK':'https://meet.google.com/tar-ejth-cfg','Maths AA HL':'https://meet.google.com/pzm-zcvz-cuz','PE':'https://g.co/meet/swamshsphe','UGC':'https://meet.google.com/dhp-xwak-zjk','Assembly':'https://meet.google.com/sdq-zmfu-goh'}
reminderDelay = 1
announcementChannel = 473402989676068906
periodDuration = 40*60
breakDuration = 10*60
#Schedule
Monday = ['2MATH','2TOK','2LANGB','2SCIENCE','1CIVICS']
Tuesday = ['2LANGA','2SCIENCE2','2ECONVA','1PE','1TOK','1CORE']
Wednesday = ['2SCIENCE2','2LANGB','2ECONVA','1UGC','2LANGA']
Thursday = ['2MATH','2LANGA','2LANGB','2SCIENCE','1ASSEMBLY']
Friday = ['2MATH','2SCIENCE','2SCIENCE2','2ECONVA','1RELIGION']
Timetable = [Monday,Tuesday,Wednesday,Thursday,Friday]
Timeslots = ['0740', '0820','0910','0950','1040','1120','1300','1340','1420','1500']
Weekdays = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4}
#Duration of each period in seconds
MATH = ['Maths AA HL','Maths AA SL','Maths AI SL']
SCIENCE = ['Physics','Biology','ESS']
SCIENCE2 = ['Chemistry','Computer Science','Business Management']
ECONVA = ['Economics','Visual Arts']
LANGA = ['English LL','English LA']
LANGB = ['Indonesian B','Chinese B','Indonesian A','Chinese A']
CIVICS = ['Civics','Indo Studies']
TOK = ['TOK']
ASSEMBLY = ['Assembly']
RELIGION = ['G12A','G12B']
PE = ['PE']
CORE = ['Core']
UGC = ['UGC']
allSubjects = [MATH,SCIENCE,SCIENCE2,ECONVA,LANGA,LANGB,CIVICS,TOK]
subjectDict = {'MATH':MATH,'SCIENCE':SCIENCE,'SCIENCE2':SCIENCE2,'ECONVA':ECONVA,'LANGA':LANGA,'LANGB':LANGB,'CIVICS':CIVICS,'TOK':TOK,'ASSEMBLY':ASSEMBLY,'RELIGION':RELIGION,'PE':PE,'CORE':CORE,'UGC':UGC}
messageCD = False
nc_CD = 1

deleteList = []
pissed = False

#Updates the global time variables
def timeRefresh():
    global cDay,cTime,cHour,cMinute,cSecond,cTotal
    Time = strftime("%a %H %M %S", localtime())
    cDay = Time[:3]
    cHour = int(Time[4:6])
    cMinute = int(Time[7:9])
    cSecond = int(Time[10:13])
    cTotal = cSecond + cMinute*60 + cHour*3600

timeRefresh()
print(cDay,cHour,cMinute,cSecond,cTotal)
#Breaks down HHMM from Timeslots list and returns tuple HH and MM
def getTime(stringTime):
    hour = stringTime[:2]
    minute = stringTime[2:]
    return hour,minute

#Finds the name of the class on the given period
def getClass(day,period):
    weekday = Weekdays.get(cDay[:3].capitalize())
    period = int(period)-1
    if period <= 5:
        classCode = Timetable[weekday][int(math.ceil((period-1)/2))]
    elif period == 6:
        classCode = Timetable[weekday][3]
    elif period == 7:
        if int(Timetable[weekday][3][0]) == 1:
            classCode = Timetable[weekday][4]
        else:
            classCode = Timetable[weekday][3]
    elif period == 8:
        classCode = Timetable[weekday][-1]
    else:
        classCode = "sNoClass"
    className = classCode[1:]
    return className

def checkWeekend():
    if cDay == ("Sat" and "Sun"):
        return True
    else:
        return False

def toHour(seconds):
    hour = int(math.floor(seconds/3600))
    minute = int(math.floor((seconds-hour*3600)/60))
    second = int(seconds-hour*3600-minute*60)
    return hour,minute,second

def timeCalibrate(delay = False):
    slotno = -1
    for slot in Timeslots:
        slotno = slotno + 1
        timeRefresh()
        #print("currently pointing at slotno: {slotno} class:{sclass}".format(slotno=slotno,sclass=getClass(cDay,slotno)))
        if cTotal > (15*3600):
            break
        slotTime = (int(slot[:2])*3600+int(slot[2:])*60)
        if cTotal > slotTime or getClass(str(cDay),slotno) == getClass(str(cDay),slotno+1):
            #print("cTotal > slotTime, skipping...")
            continue
        else:
            global reminderDelay
            if delay == True:
                tDiff = slotTime - cTotal - reminderDelay
            else:
                tDiff = slotTime - cTotal
            hDiff = toHour(tDiff)[0]
            mDiff = toHour(tDiff)[1]
            sDiff = toHour(tDiff)[2]
            break
    print("Prev: {P} Curr: {C}, Next: {N}".format(P=getClass(str(cDay),slotno-1),C=getClass(str(cDay),slotno),N=getClass(str(cDay),slotno+1)))
    next_class = getClass(str(cDay),slotno)
    return next_class,hDiff,mDiff,sDiff,tDiff,slotno


@client.event
async def on_ready():
    print("Time: {}".format(strftime("%a %H %M %S", localtime())))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Willy paying BTD6"))
    timeRefresh()
    print('{0.user} is online \n \n \n'.format(client))
    if checkWeekend() == True:
        print("Weekend. Reminders are disabled.")
    else:
        Guild = discord.utils.get(client.guilds,name="Nerds Bickering")
        print('Announcement Channel: {}'.format(discord.utils.get(Guild.channels,id=announcementChannel)))
        print('Announcement delay: {} seconds'.format(reminderDelay))
        if reminderOn == 1:
            print("Starting Reminder...")
            await reminder.start()
            print("reminder has started.")
        else:
            print("Reminder is disabled.")




#Shows what the next class is
@commands.cooldown(1, nc_CD, commands.BucketType.user)
@client.command(aliases=['n','nc'],brief="Tells what the next subject would be.")
async def nextClass(ctx):
    global deleteList
    timeRefresh()
    #If the command is called for a second time, it'll delete all the previous messages from this command
    if checkWeekend() == True:
        await ctx.send("We don't have classes during the weekend. Dumba$$.")
    else:
        calibration = timeCalibrate()
        hDiff = calibration[1]
        mDiff = calibration[2]
        sDiff = calibration[3]
        tDiff = calibration[4]
        slotno = calibration[5]
        nc = getClass(str(cDay),slotno+1)
        print(nc)
        msg1 = "Next class:   **{class_Name}**   in {hours} hours, {minutes} minutes and {seconds} seconds\n".format(class_Name=subjectDict.get(nc),hours=str(hDiff),minutes=str(mDiff),seconds=str(sDiff))
        Guild = ctx.guild
        if nc == "NoClass":
            await ctx.send("This is the last class dumbass. There's no more next class. Retard.")
        else:
            nextClasses=subjectDict.get(nc)
            print("Next class:{}".format(nc))
            #Sleeps until <reminderDelay> seconds before class starts
            messagesSent = 0
            msg2 = ""
            for classes in nextClasses:
                print("{class_Name}: <{classLink}>\n".format(class_Name=classes,classLink=linkDict.get(classes,'Missing link')))
                specifiedRole = discord.utils.get(Guild.roles,name=classes)
                if specifiedRole == None:
                    msg2 = msg2 + ("{class_Name}: <{classLink}>\n".format(class_Name=classes,classLink=linkDict.get(classes,'Missing link')))
                else:
                    msg2 = msg2 + ("{class_Name}: <{classLink}>\n".format(class_Name=specifiedRole.name,classLink=linkDict.get(specifiedRole.name,'Missing link')))
            msg = await ctx.send(msg1+msg2)
            deleteList.append(msg)
            try:
                await ctx.channel.delete_messages([ctx.message])
                await asyncio.asleep(30)
                await ctx.channel.delete_messages(deleteList)
            except:
                print("Delete error: Nothing to delete lmao")

@nextClass.error
async def nextClass_error(ctx, error):
    msgcycle = cycle(['Calm your tits','Chlll tf down','Just be patient','Damnit'])
    if isinstance(error, commands.CommandOnCooldown):
        msg = await ctx.send('{msg} {user}, try again after {cd:.1f} seconds'.format(msg=next(msgcycle),user=ctx.author.mention,cd=error.retry_after))
        await asyncio.sleep(1.5)
        await ctx.channel.delete_messages([msgd,ctx.message])
    else:
        raise error

#Important Commands\

#Sends a series of custom discord stickers arranged in a phallic shape for comedy
@commands.cooldown(1, 1, commands.BucketType.user)
@client.command(aliases=['k'])
async def kimmy(ctx):
    msgd = await ctx.send(".                         <:williepickle:818642560527630349>\n                   <:williepickle:818642560527630349><:williepickle:818642560527630349><:williepickle:818642560527630349>\n                   <:williepickle:818642560527630349><:williepickle:818642560527630349><:williepickle:818642560527630349>\n                   <:williepickle:818642560527630349><:williepickle:818642560527630349><:williepickle:818642560527630349>\n                    <:williepickle:818642560527630349><:williepickle:818642560527630349><:williepickle:818642560527630349>\n                   <:williepickle:818642560527630349><:williepickle:818642560527630349><:williepickle:818642560527630349>\n                   <:williepickle:818642560527630349><:williepickle:818642560527630349><:williepickle:818642560527630349>\n                   <:williepickle:818642560527630349><:williepickle:818642560527630349><:williepickle:818642560527630349>\n                   <:williepickle:818642560527630349><:williepickle:818642560527630349><:williepickle:818642560527630349>\n                   <:williepickle:818642560527630349><:williepickle:818642560527630349><:williepickle:818642560527630349>\n<:kimmy:818285699861184523><:kimmy:818285699861184523><:kimmy:818285699861184523>                    <:kimmy:818285699861184523><:kimmy:818285699861184523><:kimmy:818285699861184523>\n<:kimmy:818285699861184523><:kimmy:818285699861184523><:kimmy:818285699861184523>                    <:kimmy:818285699861184523><:kimmy:818285699861184523><:kimmy:818285699861184523>\n<:kimmy:818285699861184523><:kimmy:818285699861184523><:kimmy:818285699861184523>                   <:kimmy:818285699861184523><:kimmy:818285699861184523><:kimmy:818285699861184523>")
#Adds a cooldown for the command so people don't spam this too often, because
#I know they definitely will otherwise
@nextClass.error
async def kimmy_error(ctx, error):
    msgcycle = cycle(["chill dude","i'm tired","my balls itch"])
    if isinstance(error, commands.CommandOnCooldown):
        await asyncio.sleep(1.5)
        await ctx.channel.delete_messages([msgd,ctx.message])
    else:
        raise error
#Calmly tells someone to go away
@client.command(aliases=['fo'],hidden=True)
async def fuckoff(ctx):
    print("Executing FO....")
    await asyncio.sleep(30)
    await ctx.send("F**k off")
sauce_cycle = 0
prevsauce = int()
#Calmly conveys anger to someone
@client.command(aliases=['f','fu'],hidden=True)
async def fuckyou(ctx,count=1,duration=10,member=None):
    deleteList = []
    if count > 6:
        count = 6
    if member == None:
        for count in range (0,count):
            msg = await ctx.send("fuck you")
            if count > 0:
                deleteList.append(msg)
        await asyncio.sleep(duration)
        await ctx.channel.delete_messages(deleteList)
    else:
        #Specifies someone to specifically fuck
        Go = False
        IsMention = False
        person = discord.utils.get(ctx.guild.members,name=member)
        if person != None:
            Go = True
        else:
            person = discord.utils.get(ctx.guild.members,nick=member)
            if person != None:
                Go = True
            else:
                if member.startswith("<@"):
                    IsMention = True
                    Go = True
                else:
                    await ctx.send("{Member} is not in {server}!".format(Member=member,server=ctx.guild.name))
                    Go = False
        if Go == True:
            for count in range (1,count):
                if IsMention == True:
                    msg = await ctx.send("{} fuck you".format(member))
                else:
                    msg = await ctx.send("{} fuck you".format(person.mention))

            #Deletes the message to maintain secrecy and anonimity
            await asyncio.sleep(duration)
            await ctx.channel.delete_messages(deleteList)
            pissed = False
#Changes the delay (in seconds) before sending the reminder message to the channel
@client.command(aliases=['rcd','delay'],brief='Changes the delay to <Input> seconds.')
async def Delay(ctx,newDelay):
    pissed = False
    try:
        int(newDelay)
    except ValueError:
        await ctx.send("Please enter an integer number of seconds.")
    if int(newDelay) > 600:
        if pissed == True:
            #Gives the bot somewhat of an emotion by allowing it to be angry
            #If the user keeps inputting something wrong
            await ctx.send("That was not a question. Your delay is too long. Keep it below 10 minutes.")
            pissed = not pissed
        else:
            await ctx.send("Are you sure you want the reminder to come "+str(newDelay)+" seconds before class?")
            pissed = not pissed
    else:
        global reminderDelay
        reminderDelay = newDelay
        await ctx.send("The next reminder will now be sent {} seconds before class starts.".format(newDelay))
#Toggles the scheduled reminder on/off
@client.command(aliases=['tr'],brief="Toggles the scheduled reminder on/off")
async def toggleReminder(ctx):
    global reminderOn
    reminderOn = reminderOn * -1
    await ctx.send("Reminder has been "+reminder_states[reminderOn])
    if checkWeekend() == False:
        if reminderOn == 1:
            reminder.start()
        else:
            reminder.cancel()

@commands.cooldown(1, 5, commands.BucketType.user)
@client.command(aliases=['c'])
async def classNow(ctx):
    timeRefresh()
    #If the command is called for a second time, it'll delete all the previous messages from this command
    if checkWeekend() == True:
        await ctx.send("We don't have classes during the weekend. Dumba$$.")
    else:
        slotno = -1
        for slot in Timeslots:
            slotno = slotno + 1
            timeRefresh()
            #If not, then starts calculating the time for the slots
            slotTime = (int(slot[:2])*3600+int(slot[2:])*60)
            #Looping through the Timeslots list, and finds the next timeslot that is less than current time
            if cTotal > slotTime:
                continue
                #Checks if it's a double period
            else:
                break
        Guild = ctx.guild
        currentClasses=subjectDict.get((getClass(str(cDay),slotno)))
        #Sleeps until <reminderDelay> seconds before class starts
        messagesSent = 0
        msg1 = "Current classes are ***{}***\n".format(currentClasses)
        msg2 = ""
        for classes in currentClasses:
            specifiedRole = discord.utils.get(Guild.roles,name=classes)
            if specifiedRole == None:
                msg2 = msg2 + ("{class_Name}: <{classLink}>\n".format(class_Name=classes,classLink=linkDict.get(classes,'Missing link')))
            else:
                msg2 = msg2 + ("{class_Name}: <{classLink}>\n".format(class_Name=specifiedRole.name,classLink=linkDict.get(specifiedRole.name,'Missing link')))
        msg = await ctx.send(msg1+msg2)
        deleteList.append(msg)
        await asyncio.sleep(60)
        await ctx.channel.delete_messages([ctx.message])
        await ctx.channel.delete_messages(deleteList)

#Sends reminder
@client.command(aliases=['cc'],hidden=True)
async def thisChannel(ctx):
    global announcementChannel
    announcementChannel = ctx.channel
    botmsg = await ctx.send("Reminders will now be sent to "+str(ctx.channel.name)+".")
    print("Updated announcement channel.")
    print(ctx.channel.name)
    print(ctx.channel.id)
    await asyncio.sleep(3)
    await ctx.channel.delete_messages([ctx.message,botmsg])
#Logs out the bot in the case that I mess up and accidentally run the script twice,
#Causing there to be two instances of this bot running on the same server
@client.command(aliases=['logout'],hidden=True)
async def LogOut(ctx):
    msg = await ctx.send("Adios")
    await client.logout()
#In case I'm missing the links for any classes
@client.command(aliases=['ml'],brief="Shows which class links are still missing.")
async def missingLinks(ctx):
    missingLinkList = []
    for subjectgroup in allSubjects:
        for subjects in subjectgroup:
            if linkDict.get(subjects) == None:
                missingLinkList.append(subjects)
    await ctx.send("The missing subjects links are {}".format(", ".join(missingLinkList)))

@client.command(aliases=['y','Y','Yes'],hidden=True)
async def yes(ctx):
    global pissed
    if pissed == True:
        await ctx.send("That was not a question. Your delay is too long. Keep it below 10 minutes.")
        pissed = not pissed

@client.command(aliases=['cd','CD','cD','Cd'])
async def change_cd(ctx,cd):
    global nc_CD
    msg = await ctx.send("$nc cooldown has been changed from {old}s to {new}s".format(old=nc_CD,new=cd))
    nc_CD = cd
    await asyncio.sleep(1)
    await ctx.channel.delete_messages([msg,ctx.message])
@change_cd.error

async def change_cd_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        msg = await ctx.send('You forgot to mention how many seconds you want to change it to, dumba$$')
        await asyncio.sleep(0.5)
        await ctx.channel.delete_messages([msg,ctx.message])
    else:
        raise error
#Calmly tells someone to shut up
@client.command()
async def s(ctx):
    msg = await ctx.send("STFU <@!266508133474631680>")
    await ctx.channel.delete_messages([ctx.message])


#The automatic reminder
@tasks.loop(seconds=20)
async def reminder():
    global internalreminderOn
    greeting = ['Get in','Class is starting',"It's time for suffering","It's time",'The class is just starting',"Come in guys"]
    if checkWeekend() == False and internalreminderOn == True:
        #Calibrates the current time with the schedule, and calculates how much
        #time should pass before the next class begins
        calibration = timeCalibrate(True)
        nc = calibration[0]
        hDiff = calibration[1]
        mDiff = calibration[2]
        sDiff = calibration[3]
        tDiff = calibration[4]
        slotno = calibration[5]
        nc = getClass(str(cDay),slotno+1)
        Guild = discord.utils.get(client.guilds,name="Nerds Bickering")
        currentClasses=subjectDict.get(nc)
        print("Next class: {}".format(currentClasses))
        toSendChannel = discord.utils.get(Guild.channels,id=announcementChannel)
        #Sleeps until <reminderDelay> seconds before class starts, then sends the message
        print("tDiff: {tDiff}   reminderDelay: {reminderDelay}".format(tDiff=tDiff,reminderDelay=reminderDelay))
        print("Sleeping for {h} hours {m} minutes and {s} seconds...".format(h=hDiff,m=mDiff,s=sDiff))
        await asyncio.sleep(tDiff-reminderDelay)
        if reminderOn == 1:
            messagesSent = 0
            lines = "***{}***\n".format(greeting[randint(0,len(greeting)-1)])
            for classes in currentClasses:
                specifiedRole = discord.utils.get(Guild.roles,name=classes)
                if specifiedRole == None:
                    lines = lines + "{class_Name}: <{classLink}>\n".format(class_Name=currentClasses,classLink=linkDict.get(currentClasses,'Missing link'))
                else:
                    lines = lines + "{class_Name}: <{classLink}>\n".format(class_Name=specifiedRole,classLink=linkDict.get(specifiedRole.name,'Missing link'))
            print("Sending reminders")
            print("=====================================")
            msg = await toSendChannel.send(lines)
            internalreminderOn = False
            print("Reminder will be halted for {} seconds".format(periodDuration/2))
            await asyncio.sleep(10)
            #Waits for a certain time before deleting the messages
            internalreminderOn = True



client.run(TOKEN)
