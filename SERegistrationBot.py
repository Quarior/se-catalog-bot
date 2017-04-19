import discord
import locale
import asyncio
import random
import requests
import time
import json
from operator import itemgetter
import sc_to_json
from bs4 import BeautifulSoup 


# Startup and reference values
client = discord.Client()
token = 'MzA0MTg4NDEwMDA2ODYzODcy.C9jxmw.4_JYxDjJ9wRXs5r7Hk5e2LUI3Ew' #token of the bot
channel = '302933532563734530'
#Input
Register = ';register'
Score = ';score'
Systems = ';systems'
Help = ';help'
#Locale
Locale = locale.getdefaultlocale()
#English default strings
#Register
StrCachingFile = 'Caching file...'
Strbm = ' **Congratulations in uploading your first system ! You earned a 1.5x multiplier for first time !**'
Stredited_message = '{0} registered to database.\n{1} bodies registered with {2} stars and {3} planets.\n{4} points have been added to {5}\'s account.\nCurrent : {7} points.{6}'
StrSorry = "Sorry, that system had already been discovered by {0}!"
StrErrorRegister = 'Register in the format :\n```{0} (link to .sc file) (system name)```'
StrWait = "{0}, please wait another {1} seconds before registering another system."
#Score
StrScore1 = "{0}, you currently have {1} points from {2} systems."
StrScore0 = "{0}, you have not registered a single system. Use {1} to register an exported system !"
#Systems
StrSystems = '{0}. {1} - {2} Stars and {3} planets ({4} points)'
StrSystemsMore = 'and {0} more...'
StrSystems0 = "You have no registered systems."
#Help
StrHelp = "Use {0} (link) (system name) to register a system, {1} to see your score, and {2} to see your registered systems !\nIn order to upload a system, use the \"Export System\" option and upload the .sc file to Discord before getting the link !"
#On_ready
StrOnReady = 'I\'m online, use {0} to register your systems !'
#Translation
if Locale[0] == "fr_FR":
    #French strings
    #Register
    StrCachingFile = 'Fichier de mise en cache...'
    Strbm = ' **Félicitations pour télécharger votre premier système ! Vous avez gagné un multiplicateur 1.5x pour la première fois !**'
    Stredited_message = '{0} enregistré à la base de donnée.\n{1} astres enregistrés avec {2} étoiles et {3} planètes.\n{4} points ont été ajoutés au compte de {5}.\nActuellement : {7} points.{6}'	
    StrSorry = "Désolé, ce système a déjà été découvert par {0}!"
    StrErrorRegister = 'Enregistrer dans ce format :\n```{0} (lien au fichier .sc) (nom du système)```'
    StrWait = "{0}, veuillez attendre {1} secondes avant d'enregistrer un autre système."
    #Score
    StrScore1 = "{0}, vous avez actuellement {1} points à partir de {2} systèmes."
    StrScore0 = "{0}, vous avez actuellement aucun point. Utilisez {1} pour enregistrer un système exporté."
    #Systems
    StrSystems = '{0}. {1} - {2} Etoiles et {3} planètes ({4} points)'
    StrSystemsMore = 'et {0} autres...'
    StrSystems0 = "Vous n'avez pas enregistrer de systèmes."
    #Help
    StrHelp = "Utilisez {0} (lien) (nom du système) pour enregistrer un système, {1} pour voir votre score, et {2} pour voir vos systèmes enregistrés !\nDans l'ordre pour charger un système, utiliez l'option \"Exporter le système\" et charger le fichier .sc sur Discord avant de donner le lien !"
    StrOnReady = 'Je suis en ligne, utiliser {0} pour enregistrer vos systèmes !'
	
#Program
# All data titles are in proper cases i.e. Data Titles or command e.g. ;asteroid

def check_for_os(string):
    if 'os' in string.replace('.',' ').split():
        return True
    else:
        return False

def jsonwrite(json_dic, datafile):
    with open(datafile, 'w') as target:
        json.dump(json_dic, target, indent=4, separators=(',',':'))
    
with open('explorer_data.json') as scoreboard:
    score = json.load(scoreboard)

@client.event
async def on_message(message):
    if message.author != client.user:
        maid = message.author.id

        # Register a system
        if message.content.startswith(Register):
            time_list = score['time']
            if message.author.id in list(time_list.keys()):
                last = time_list[message.author.id]
            else:
                last = 0
            time_passed = time.time()- last
            if time_passed > 300:
                part = message.content.split()
                if len(part) > 1:
                    file = part[1]
                    if file.startswith('https://') and file.endswith('.sc'):
                        systemname = file.split('/')[-1].replace('.sc','').replace('_',' ')
                        if systemname not in score['system_list']:
                            opened = requests.get(file).text
                            messaged = await client.send_message(message.channel, StrCachingFile)
                            cache_name = 'cache' + '.txt' 
                            with open(cache_name, 'w') as cache_file:
                                cache_file.write(opened)
                            if len(part) > 2:
                                nickname = ' '.join(part[2::])
                            else:
                                nickname = systemname
                            res = sc_to_json.to_json(cache_name, 'se_data', systemname, nickname)
                            op_js = res[0]
                            t_v = res[1]
                            b_c = 0
                            for key in op_js['body_count'].keys():
                                b_c += op_js['body_count'][key]
                            if 'Star' in list(op_js['body_count'].keys()):
                                s_c = str(op_js['body_count']['Star'])
                            else:
                                s_c = 0
                            if 'Planet' in list(op_js['body_count'].keys()):
                                p_c = str(op_js['body_count']['Planet'])
                            else:
                                p_c = 0
                            if maid in list(score['users'].keys()):
                                score['users'][maid]['systems_discovered'] += 1
                                score['users'][maid]['points'] += t_v
                                sys_score = int(t_v)
                                score['users'][maid]['username'] = message.author.name
                                score['system_list'][systemname] = op_js
                                bm = ''
                            else:
                                score['users'][maid] = {}
                                score['users'][maid]['systems_discovered'] = 1
                                sys_score = int(int(t_v)*1.5)
                                score['users'][maid]['points'] = sys_score
                                score['users'][maid]['username'] = message.author.name
                                score['system_list'][systemname] = op_js
                                bm = "\n" + Strbm
                            cur_sc = score['users'][maid]['points']
                            reg_time = time.time()
                            score['system_list'][systemname]['value'] = int(t_v)
                            score['time'][message.author.id] = reg_time
                            score['system_list'][systemname]['nick'] = nickname
                            score['system_list'][systemname]['time_discovered'] = reg_time
                            score['system_list'][systemname]['discovered_by'] = message.author.id
                            jsonwrite(score, 'explorer_data.json')
                            edited_message = Stredited_message.format(nickname, b_c, s_c, p_c, sys_score, message.author.mention, bm, cur_sc)
                            await client.edit_message(messaged, edited_message)
                        else:
                            await client.send_message(message.channel, StrSorry.format(message.author.display_name))
                else:
                    await client.send_message(message.channel, StrErrorRegister.format(Register))
            else:
                await client.send_message(message.channel, StrWait.format(message.author.mention, int(300-time_passed)))

        # See balance
        elif message.content == Score:
            if maid in list(score['users'].keys()):
                await client.send_message(message.channel, StrScore1.format(message.author.mention, score['users'][maid]['points'], score['users'][maid]['systems_discovered']))
            else:
                await client.send_message(message.channel, StrScore0.format(message.author.mention, Register)) 
        # List systems
        elif message.content == Systems:
            if maid in list(score['users'].keys()):
                sy = score['system_list']
                print([k for k in sy])
                sr = [sy[k] for k in sy if sy[k]['discovered_by'] == maid]
                sl = []
                for sdic in sr:
                    sl.append(StrSystems.format(sr.index(sdic)+1,sdic['nick'],
                                                                                        sdic['body_count']['Star'],
                                                                                        sdic['body_count']['Planet'], sdic['value']))     
                s = '```{0}```'.format('\n'.join(sl))
                c = 0
                while len(s) > 1999:
                    sl = sl[1:] 
                    c += 1
                    s = '```{0}```'.format('\n'.join(sl))
                await client.send_message(message.channel, s)
                if c != 0:
                    await client.send_message(message.channel, StrSystemsMore.format(c))
            else:
                await client.send_message(message.channel, StrSystems0)
        
        elif message.content == Help:
            await client.send_message(message.channel, StrHelp.format(Register, Score, Systems))
                            
#Just to know it's running    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(client.get_channel(str(channel)), StrOnReady.format(Register))
        

#Runs the whole thing
client.run(token)
