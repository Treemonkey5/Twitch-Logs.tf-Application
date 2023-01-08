import requests,json,asyncio 
from twitchio.ext import commands
import zipfile,io
import re

def validstream(S):

    if len(S)==0:
        return False
    elif S[0].game_name != "Team Fortress 2":
        return False
    else:
        return True
            
def getlogs(url):

    req=requests.get(url).text
    logs=json.loads(req)
    return [logs["logs"][0]["id"],logs["logs"][1]["id"],logs["logs"][2]["id"]]

def validlog(id):
    url='https://logs.tf/logs/log_%s.log.zip' %(id)

    req=requests.get(url)
    z=zipfile.ZipFile(io.BytesIO(req.content))

    info=(z.infolist()[0])
    last_lines=str(z.read(info)).split("\\nL")

    x=(re.search("(\d\d:){3}",last_lines[0]).group()).split(":")
    y=(re.search("(\d\d:){3}",last_lines[-1]).group()).split(":")
    

    ytime=int(y[0])*3600 + int(y[1]) *60 +int(y[2])
    xtime=int(x[0])*3600 + int(x[1]) *60 +int(x[2])

    if ytime-xtime <180:
        return False

    try:
        endlines=[last_lines[-5],last_lines[-4],last_lines[-3],last_lines[-2],last_lines[-1],last_lines[-0]]
    except:
        return False

    for i in endlines:
        if "[P-REC]" in i:
            return(True)

    return False

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='oauth:zvrqpxk8car3wximfo5klth51lqlg2', prefix='!', initial_channels=['Treemonker','squidie_','minicirclex'])



    async def event_message(self,message):
        if message.echo:
            return

        await bot.handle_commands(message)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

        Channels=[]
        Streams=[]
        url=[]
        Check=[]

        for i in bot.connected_channels:
            Channels.append(i)
        for C in Channels:
            Streams.append(await bot.fetch_streams([(await C.user()).id]))

        
        FILE=open("C:\\Users\\Parker\\Documents\\twitch bot\\Channels.txt","r")   
        db=FILE.read().split(",")
        FILE.close()

        for i in db:
            tmp=i.split("/")
            url.append('http://logs.tf/api/v1/log?player=%s' %(tmp[1]))
        
        for i in url:
            Check.append(getlogs(i))


        while True:
            for i in range(len(Streams)):
                if validstream(Streams[i]):
                    print("valid")
                    new_check=getlogs(url[i])

                    if new_check[0]==Check[i][0]:
                        await asyncio.sleep(10)

                    else:
                        for k in range(3):
                            if new_check[k] not in Check[i]:
                                if validlog(new_check(k)):
                                    await Channels[i].send("CodeMongus - http://logs.tf/%s" %(new_check[1]))
            Streams.clear()
            for C in Channels:
                Streams.append(await bot.fetch_streams([(await C.user()).id]))


    @commands.command()
    async def log(self,ctx):
        

        FILE=open("C:\\Users\\Parker\\Documents\\twitch bot\\Channels.txt","r")   
        db=FILE.read().split(",")
        FILE.close()
        id=0

        for i in db:
            if i.startswith(ctx.channel.name):
                id=i[len(ctx.channel.name)+1:]
                

        url='http://logs.tf/api/v1/log?player=%s' %(id)
        req=requests.get(url).text
        logs=json.loads(req)

        await ctx.send("CodeMongus - http://logs.tf/%s" %(logs["logs"][0]["id"]))


     

bot=Bot()
bot.run()