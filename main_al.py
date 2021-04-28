import os
import discord
import requests
import json
from keep_alive import keep_alive


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def ani(q, author,M_flag):
    if M_flag == 0:
        query = '''
        query ($search: String) { # Define which variables will be used in the query (id)
        Media (search: $search, type: ANIME) { # Insert our variables into the query arguments (search)
                title {
            romaji
            }
            type
            format
            episodes
            status
            genres
            description
            coverImage{
                medium
            }
            siteUrl
        }
        }
        '''
    else:
        query = '''
        query ($search: String) { # Define which variables will be used in the query (id)
        Media (search: $search, type: MANGA) { # Insert our variables into the query arguments (search)
            title {
            romaji
            }
            type
            format
            chapters
            volumes
            status
            genres
            description
            coverImage{
                medium
            }
            siteUrl
        }
        }
        '''
    # Define our query variables and values that will be used in the query request
    variables = {
        'search': q
    }
    url = 'https://graphql.anilist.co'
    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = json.loads(response.text)
    if data["data"]["Media"] == None:
        error = discord.Embed(
            title="Title not found"
        )
        error.set_image(url = "https://media1.tenor.com/images/0c143322f7e7d772353a965720338aa4/tenor.gif?itemid=19978494")
        return error
    title = data["data"]["Media"]["title"]["romaji"]
    para=""
    if data["data"]["Media"]["description"] != None:
      para = remove_html_tags(data["data"]["Media"]["description"])
    type_ = data["data"]["Media"]["type"]
    format_ = data["data"]["Media"]["format"]
    if M_flag == 0:
        episodes = str(data["data"]["Media"]["episodes"])
    else: 
        chapters = str(data["data"]["Media"]["chapters"])
        volumes = str(data["data"]["Media"]["volumes"])
    status = data["data"]["Media"]["status"]
    genres=""
    for element in data["data"]["Media"]["genres"]:
        genres +=element + ' '
    cover_image= data["data"]["Media"]["coverImage"]["medium"]
    url = data["data"]["Media"]["siteUrl"]


    content = "\n" + para + "\n\n"
    if M_flag == 0:
        stats = "Type: " + type_ + "\nFormat: " + format_ + "\nEpisodes: " + episodes + "\nStatus: " + status + "\nGenres: " + genres
    else:
        stats = "Type: " + type_ + "\nFormat: " + format_ + "\nChapters: " + chapters + "\nVolumes: " + volumes + "\nStatus: " + status + "\nGenres: " + genres
            
    embed = discord.Embed(
        title=title,
        url=url,
        description = content,
        color = discord.Colour.red()
    )
    embed.add_field(name="Information", value = stats, inline = False)
    embed.set_thumbnail(url=cover_image)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed       

def mov(q, author,T_flag):
    key = os.environ["api_key"]
    
    if T_flag == 0:
        url = "http://www.omdbapi.com/?t=" + q + "&type=movie&apikey=" + key
    else:
        url = "http://www.omdbapi.com/?t=" + q + "&type=series&apikey=" + key    
    response = requests.get(url)
    data = response.json()
    if data["Response"] == "False":
        error = discord.Embed(
            title="Title not found"
        )
        error.set_image(url = "https://cdn.discordapp.com/attachments/637008973714817027/834462141267705976/remicry.gif")
        return error

    title = data["Title"]
    poster = data["Poster"]
    year = data["Year"]
    genres = data["Genre"]
    director = data["Director"]
    writer = data["Writer"]
    actors = data["Actors"]
    para = data["Plot"]
    score = data["imdbRating"]
    type_ = data["Type"]
    id_ = data["imdbID"]
    url_ = "https://www.imdb.com/title/" + id_
    
    if T_flag == 1:
      seasons = data["totalSeasons"]
    stats = "Type: " + type_ + "\nRating: " + str(score) + "\nYear: " + year +''' "\nSeasons: " + str(seasons) + '''"\nDirector: " + director + "\nActors: " + actors + "\nGenres: " + genres      
    content = "\n" + para[:2048] + "\n\n"
    if T_flag == 0:
      stats = "Type: " + type_ + "\nRating: " + str(score) + "\nYear: " + year + "\nDirector: " + director + "\nActors: " + actors + "\nGenres: " + genres
    else: 
      stats = "Type: " + type_ + "\nRating: " + str(score) + "\nYear: " + year +"\nSeasons: " + seasons + "\nWriter: " + writer + "\nActors: " + actors + "\nGenres: " + genres  
    embed = discord.Embed(
        title=title,
        url=url_,
        description = content,
        color = discord.Colour.green()
    )
    embed.add_field(name="Information", value = stats, inline = False)
    embed.set_thumbnail(url=poster)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed

def book(q, auth):
  response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + q)
  data = json.loads(response.text)
  if data["totalItems"] == 0:
        error = discord.Embed(
            title="Book not found"
        )
        error.set_image(url = "https://cdn.discordapp.com/attachments/637008973714817027/834462141267705976/remicry.gif")
        return error
  title=""
  if "title" in  data["items"][0]["volumeInfo"].keys():      
    title = data["items"][0]["volumeInfo"]["title"]
  para=""
  if "description" in  data["items"][0]["volumeInfo"].keys(): 
    para = data["items"][0]["volumeInfo"]["description"]
  if len(para) > 750:
      para = para[:750] + "..."
  date_ =""
  if "publishedDate" in  data["items"][0]["volumeInfo"].keys(): 
    date_ = data["items"][0]["volumeInfo"]["publishedDate"]
  authorlst=[]
  if "authors" in  data["items"][0]["volumeInfo"].keys():   
    authorlst = data["items"][0]["volumeInfo"]["authors"]
  author=""
  for element in authorlst:
      author +=element + ", "
  id_ = data["items"][0]["id"]
  cover_image = "https://www.messagetech.com/wp-content/themes/ml_mti/images/no-image.jpg"
  if "imageLinks" in  data["items"][0]["volumeInfo"].keys():
    if "thumbnail" in  data["items"][0]["volumeInfo"]["imageLinks"].keys():
      cover_image = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
  url = "http://books.google.com/books?id=" + id_
  categorylst=[]
  if "categories" in  data["items"][0]["volumeInfo"].keys(): 
    categorylst = data["items"][0]["volumeInfo"]["categories"]
  categories=""
  for element in categorylst:
      categories += element + " " 
  content = "\n" + para + "\n\n"
  stats = "Author: " + author + "\nPublishing Date: " + date_ + "\nCategories: " + categories
  embed = discord.Embed(
    title=title,
    url = url,
    description = content
  )
  embed.add_field(name="Information", value = stats, inline = False)
  embed.set_thumbnail(url=cover_image)
  embed.set_footer(icon_url=auth.avatar_url, text=f"Requested by {auth.name}")
  return embed    

def hel(author):
    embed = discord.Embed(
        title="Help Page",
        description = "List of available commands"
    )
    embed.add_field(name="Anime", value="r!anime <query>", inline=False)
    embed.add_field(name="Manga", value="r!manga <query>", inline=False)
    embed.add_field(name="TV Show", value="r!tv <query>", inline=False)
    embed.add_field(name="Movie", value="r!movie <query>", inline=False)
    embed.add_field(name="Book", value="r!book <query>", inline=False)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content    
    
    if msg.startswith('r!help'):
        await message.channel.send(embed = hel(message.author))
    lst = msg.split()
    if len(lst) == 0:
      return
    prefix=lst.pop(0)
    q = ' '.join(lst)        
    
    if prefix == "r!anime":
        await message.channel.send(embed = ani(q, message.author, 0))
    elif prefix == "r!manga":
        await message.channel.send(embed = ani(q, message.author, 1))
    elif prefix == "r!movie":
        await message.channel.send(embed = mov(q, message.author,0))
    elif prefix == "r!tv":
        await message.channel.send(embed = mov(q, message.author,1))
    elif prefix == "r!book" or prefix == "r!books":
        await message.channel.send(embed = book(q, message.author))
    
keep_alive()
client.run(os.environ['TOKEN'])
