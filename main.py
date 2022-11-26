import discord, random, json, requests, time, pytz, datetime, mendeleev, wikipedia, bs4, urllib, urllib3
from discord.ext import commands, tasks
from itertools import cycle
from pytz import timezone
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

status = cycle(["never gonna give you up", "never gonna let you down"])

TOKEN = ('xxxxxxxxxxxxxxxxxxxxxx')

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    change_status.start()
    print("Hello world!")


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def hi(ctx):
    await ctx.send('hi')


try:
    dog = requests.get("https://dog-facts-api.herokuapp.com/api/v1/resources/dogs/all")
    dogfact = dog.json()


    @client.command(aliases=["randomdogfact"])
    async def rdf(ctx):
        random_fact = random.choice(dogfact)["fact"]
        await ctx.send(random_fact)
except:
    pass


@client.command()
async def ami(ctx, *, question):
    answers = [f"Yes, you are {question}.",
               f"No, you are not {question}.",
               f"I don't know, ask your mom whether you're {question}.",
               f"Do you seriously believe I think you're {question}?",
               f"Hahahaha, you will never be {question}!"]
    await ctx.send(random.choice(answers))

@client.command()
async def howcuteis(ctx, *, namecute):
    percentcute = random.randint(100, 10000)
    await ctx.send(f"{namecute.capitalize()} is {percentcute}% cute.")

@client.command()
async def say(ctx, *, saythis):
    await ctx.send(f"{saythis}")
    await ctx.message.delete()


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return

    if any(word in message.content.lower() for word in ["i love u", "i love you", "i lov u"]):
        await message.channel.send("I love you too!")

    if message.content.lower().startswith(("hi", "hey", "hello")):
        await message.channel.send("Hey :)")

    if 'no u' in message.content.lower():
        await message.channel.send("no u")


@client.command()
async def info(ctx):
    aboutslavio = discord.Embed(title="About Me", description="Hi I'm Slavio, it's nice to meet you!", colour=0x1f004d)
    aboutslavio.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/889829697482031108/890158188559749150/f8c7dbf7a2ce6f245c7d2f3b31382.jpeg")
    aboutslavio.add_field(name="Owners", value="Nee, Ward", inline=True)
    aboutslavio.add_field(name="Birthday", value="19th September 2021", inline=True)
    await ctx.send(embed=aboutslavio)


client.remove_command('help')


@client.command(aliases=['help'])
async def _help(ctx):
    helpslavio = discord.Embed(title="Help me stepbot I'm confused :(",
                               description="Type ! followed by one of the commands from the list of commands below (no space between ! and the command). \n ** ** \n ** **",
                               colour=0x1f004d)
    helpslavio.add_field(name="List of Commands",
                         value=
                         "\n ** ** \n "
                         "*__info__*    ———>    *tells you some stuff about the bot* \n"
                         "\n *__hi__*    ———>    *says hi, mainly a test to see if the bot is working* \n"
                         "\n *__rdf__*    ———>    *displays a random dog fact* \n"
                         "\n *__amicute__*    ———>    *I don't know, are you?* \n"
                         "\n *__ami (insertthinghere)__*    ———>    *tells you whether you're (insertthinghere)* \n"
                         "\n *__howcuteis (insertthinghere)__*    ———>    *tells you how cute (insertthinghere) is* \n"
                         "\n *__say__*    ———>    *says whatever you make the bot say, use this power wisely* \n"
                         "\n *__waifu__*    ———>    *your very own AI-generated waifu!* \n"
                         "\n *__uselesswiki__*    ———>    *the reason your teacher told you wikipedia isn't a valid source* \n"
                         "\n *__wyr__*    ———>    *a little would you rather minigame* \n")
    await ctx.send(embed=helpslavio)

@client.command()
async def uselesswiki(ctx, *, search):
    try:
        page = wikipedia.summary(f"{search}")
        await ctx.send(f"{page}")
        # page = wikipedia.summary(f"{search}")
        # wikembed = discord.Embed(title="title", description=f"{page}")
        # wikembed.set_image(url=f"wikipedia.page(search).images[0]")
        # await ctx.send(embed=wikembed)

    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options
        response_text = "Which one of these were you looking for?" + "\n"
        for i, optionswithnumbers in enumerate(options):
            response_text += f"{i}) {optionswithnumbers}" + "\n"
        response_text += "Please type the number corresponding to the article you were looking for" + "\n"
        await ctx.send(response_text)
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        choice = int(msg.content)
        await ctx.send(f"{wikipedia.summary(options[choice])}")
    except:
        await ctx.send("i give up")


@client.command()
async def whattimeisit(ctx, name):
    if name in usertimezones.keys():
        tz = pytz.timezone((usertimezones[name]))
        timenow = datetime.datetime.now(tz).strftime("%H:%M")
        await ctx.send(f"It is currently {timenow} for {name}")
    else:
        await ctx.send(f"Sorry, no timezone has been registered for {name}")


@client.command()
async def waifu(ctx):
    waifupic = random.randint(0, 100000)
    waifu_embed = discord.Embed(title="Here's your random AI-generated waifu!", colour=0x1f004d)
    waifu_embed.set_image(url=f"https://www.thiswaifudoesnotexist.net/example-{waifupic}.jpg")
    await ctx.send(embed=waifu_embed)


dictionary = requests.get(
    "https://www.dictionaryapi.com/api/v3/references/collegiate/json/voluminous?key=xxxxxxxxxxxxxxxxxxxxxxxx")
thesaurus = requests.get(
    "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/umpire?key=xxxxxxxxxxxxxxxxxxxxxx")

dictionary_api = dictionary.json()
thesaurus_api = thesaurus.json()

# print(random.choice(dictionary.json()))

f = open("filtered_words.json")
words = json.load(f)

# want to select parts of this data
@client.command(aliases=['rw', 'word', 'wotd'])
async def randomword(ctx):
    rw = random.choice(words)
    wordtodefine = requests.get(
        f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{rw}?key=xxxxxxxxxxxxxxxxxxxxxxxx")
    defineword = wordtodefine.json()
    definedword = ""
    for i, deflist in enumerate(defineword[0]['shortdef'], start=1):
        definedword += f"{i}] {deflist}\n\n "

    def_embed = discord.Embed(title=f"{rw.capitalize()}", description=f"{definedword}", colour=0x1f004d)

    await ctx.send(embed=def_embed)


@client.command(aliases=['def', 'df'])
async def define(ctx, search):
    wordtodefine = requests.get(
        f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{search}?key=xxxxxxxxxxxxxxxxxxxxxxxxx")
    defineword = wordtodefine.json()
    definedword = ""
    for i, deflist in enumerate(defineword[0]['shortdef'], start=1):
        definedword += f"{i}] {deflist}\n\n "

    def_embed = discord.Embed(title=f"{search.capitalize()}", description=f"{definedword}", colour=0x1f004d)

    await ctx.send(embed=def_embed)


file = open("wyr_questions.txt", "r", encoding="utf-8")
wyrq = []
for line in file.readlines():
    line = line.rstrip("\n")
    if (line != ""):
        line_parts = line.split(" ")
        line_parts.pop(0)
        line = " ".join(line_parts)
        wyrq.append(line)


@client.command()
async def wyr(ctx):
    wyrembed = discord.Embed(description=f"{random.choice(wyrq)}", colour=0x1f004d)
    await ctx.send(embed=wyrembed)


usertimezonedictionary = {}
try:
    file = open("usertimezoneslist.json", "r")
    usertimezonedictionary = json.load(file)
except Exception:
    usertimezonedictionary = {}
file.close()


@client.command()
async def settz(ctx):
    global usertimezonedictionary

    reply1 = "Choose your region: \n \n"
    regions = ["Africa", "America", "Asia", "Atlantic", "Australia", "Canada", "Europe", "US"]
    tz = pytz.common_timezones
    for i, regions_list in enumerate(regions, start=1):
        reply1 += f"{i}] {regions_list}  \n "
    await ctx.send(f"{reply1}")

    awaitreply1 = await client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
    usertz = regions[int(awaitreply1.content) - 1]
    variableregion = []
    for userregion in tz:
        if userregion.startswith(usertz):
            variableregion.append(userregion)

    print(variableregion)
    reply2 = "Choose your timezone: \n \n"
    for i, tz_list in enumerate(variableregion, start=1):
        reply2 += f"{i}] {tz_list}  \n "
        if i % 50 == 0 and i > 0:
            print("Presending")
            await ctx.send(reply2)
            reply2 = ""
    await ctx.send(f"{reply2}")

    awaitreply2 = await client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
    actualusertz = variableregion[int(awaitreply2.content) - 1]
    usertimezonedictionary[f"{ctx.author.id}"] = f"{actualusertz}"

    print(usertimezonedictionary)
    await ctx.send(f"Success! Your timezone has been registered as: {actualusertz}")

    file = open("usertimezoneslist.json", "w")
    json.dump(usertimezonedictionary, file)
    file.close()


@client.command()
async def timenow(ctx, user: discord.User):
    idofuser = str(user.id)
    if idofuser in usertimezonedictionary:
        timezoneofuser = pytz.timezone(usertimezonedictionary[idofuser])
        time = datetime.datetime.now(timezoneofuser).strftime("%H:%M")
        await ctx.channel.send(f"It is currently {time} for {user.name}.")
    else:
        await ctx.channel.send(f"The user's timezone has not been registered.")


@client.command(name="quote", aliases=['fakequote', 'fq'])
async def quote(ctx, user: discord.User, *, quote):
    date = datetime.date.today().strftime("%d %B %Y")
    quote_embed = discord.Embed(description=f'> {quote}' f"\n  **    ** *- {user.name}, {date}*")
    quote_embed.set_author(name=f"{user.display_name}", icon_url=f"{user.avatar_url}")
    await ctx.send(embed=quote_embed)


ud_api_url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"


def create_embed(data, number, search):
    ud_definition = data['list'][number]['definition']
    ud_author = data['list'][number]['author']
    ud_example = data['list'][number]['example']
    ud_date = data['list'][number]['written_on'][:-14]
    ud_votes = data['list'][number]['thumbs_up']

    embed = discord.Embed(title=f"{search}", colour=0x1f004d)

    embed.add_field(name="Definition", value=f"{ud_definition}", inline=False)
    embed.add_field(name="Examples", value=f"{ud_example}", inline=False)
    embed.add_field(name="Date Written", value=f"{ud_date}", inline=True)
    embed.add_field(name="Author", value=f"{ud_author}", inline=True)
    embed.add_field(name="Votes", value=f"{ud_votes}", inline=True)
    embed.add_field(name="Page", value=f"{number + 1}", inline=True)

    return embed


@client.command()
async def wiki(ctx, *, search):
    search.replace(" ", "+")
    print(headers)
    r = requests.get(f"https://www.google.com/search?q=wikipedia+{search}", headers=headers, cookies=cookies)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    alllinks = soup.find_all('a')
    # print(alllinks)
    links = []
    for i in alllinks:
        links.append(i.get('href'))
    actuallink = 0
    print(links)
    while True:
        for i in links:
            if 'https://en.wikipedia.org/wiki/' in str(i):
                actuallink = i
                break
        break
    string = actuallink.replace("/url?q=", "")
    split_string = string.split("&")
    wikiurlookingfor = split_string[0]
    await ctx.send(f"{wikiurlookingfor}")


@client.command()
async def weather(ctx, *, search):
    search.replace(" ", "+")
    tempreq = requests.get(f"https://www.google.com/search?q=weather+in+{search}", headers=headers, cookies=cookies)
    tsoup = bs4.BeautifulSoup(tempreq.text, "html.parser")
    temp = tsoup.find("span", id='wob_tm').text
    await ctx.send(f"{temp}°C")


@client.command()
async def search(ctx, *, search):
    search.replace(" ", "+")
    searchreq = requests.get(f"https://www.google.com/search?q={search}", headers=headers, cookies=cookies)
    searchsoup = bs4.BeautifulSoup(searchreq.text, "html.parser")
    search_results = searchsoup.find("div", class_='Z0LcW', ).text
    await ctx.send(f"{search_results}")


@client.command(aliases=['el'])
async def elements(ctx, search):
    elsearch = search.capitalize()
    el = element(f'{elsearch}')
    el_embed = discord.Embed(title=f"{el.name.capitalize()}", description=
    f'**Name:** {el.name} [{el.symbol}]'
    f'\n**Atomic Number:** {el.atomic_number}'
    f'\n**Atomic Weight:** {el.atomic_weight}'
    f'\n**Electronic Configuration:** {el.econf}'
    f'\n**Oxidation States:** {el.oxistates}'
    f'\n**Position:** Group {el.group_id}, Period {el.period}, {el.block}-block'
    f'\n**Series:** {el.series}'

    f'\n\n**Description:** {el.description}'
    f'\n**Sources:** {el.sources}'
    f'\n**Uses:** {el.uses}'

    f'\n\n**Lattice Structure:** {el.lattice_structure}'
    f'\n**Atomic Radius:** {el.atomic_radius} pm'
    f'\n**Boiling Point:** {el.boiling_point} K'
    f'\n**Melting Point:** {el.melting_point} K'
    f'\n**Electron Affinity:** {el.electron_affinity} eV')
    await ctx.send(embed=el_embed)


@client.command(aliases=['urbandictionary', 'urban'])
async def ud(ctx, *, search):
    ud_headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
    try:
        number = 0
        ud_api_querystring = {"term": f"{search}"}
        search_ud = requests.request("GET", ud_api_url, headers=ud_headers, params=ud_api_querystring)
        search_ud_json = search_ud.json()

        ud_embed = create_embed(search_ud_json, number, search)

        msg = await ctx.send(embed=ud_embed)
        left_arrow = '⬅'
        await msg.add_reaction(left_arrow)
        right_arrow = '➡'
        await msg.add_reaction(right_arrow)
        ud_embed_test = discord.Embed(description="this is a test")

        while True:
            reaction, user = await client.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id, timeout=60)
            if str(reaction.emoji) == '➡':
                try:
                    number = number + 1
                    ud_embed = create_embed(search_ud_json, number, search)
                    await msg.edit(embed=ud_embed)
                except:
                    number = -1
            elif str(reaction.emoji) == '⬅':
                try:
                    if number > 0:
                        number = number - 1
                        ud_embed = create_embed(search_ud_json, number, search)
                        await msg.edit(embed=ud_embed)
                    else:
                        pass
                except:
                    pass
            else:
                break
    except:
        ud_not_found = discord.Embed(description="Sorry, the page you requested wasn't found.", colour=0x1f004d)
        await ctx.send(embed=ud_not_found)



langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
langsdict = langs_dict.items()
langlist = ""
for key, value in langsdict:
    keycap = key.capitalize()
    langlist += f"{keycap} = {value} \n"
@client.command(aliases=['trlanglist', 'langlist'])
async def trll(ctx):
    langlist_embed = discord.Embed(description=f"{langlist}", colour=0x1f004d)
    await ctx.send(embed=langlist_embed)

@client.command(aliases=['translate'])
async def tr(ctx, srclang, trglang, *, search):
    translatedtoenglish = GoogleTranslator(source=f'{srclang}', target=f'{trglang}').translate(f"{search}")
    await ctx.send(f"{translatedtoenglish}")

client.run(TOKEN)
