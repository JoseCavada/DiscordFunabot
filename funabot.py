
import discord #api discord
import os
#from replit import db #database de replit
import pickledb
#definiendo bases del bot
my_secret = #clave privada de api de discord
client = discord.Client()
#archivo de base de datos pickledb, si no existe, se crea
db = pickledb.load('funados.db', True)
#agrega una funa a la base de datos, primero busca Id repetido, si no existe, la crea, si existe, aumenta el contador en 1
def agregarFuna (idFunado):
  if idFunado in db.getall():
    numFunas = db.get(idFunado) + 1
    db.set(idFunado,numFunas)
  else:
    db.set(idFunado, 1)

#recupera el nombre del funado mediante la Id dada
async def funadoName(funadoId):
  funadoNum = await client.fetch_user(funadoId)
  size = len(str(funadoNum))
  funadoFormated = str(funadoNum)[:size-5]
  return funadoFormated
 

#aviso en consola que el bot está vivo
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
#sucede cuando ocurre un mensaje
@client.event
async def on_message(message):
  if message.author == client.user:
        return
  
  #Si el mensaje empieza por "!funados" Se recupera la lista de todos los funados y se muestran en pantalla. Primero crea una lista con todos los datos guerdados en la bs, y luego gracias al metodo funadoName() transforma las Id's guerdadas en nombres y las lista
  if message.content.startswith('!funados'):
    mensaje = ""
    for key in db.getall():
      funadoId = key
      print(f'{key} funado {db.get(key)} veces')
      mensaje =mensaje + f"\n\n-{await funadoName(funadoId)} ha sido funado {db.get(key)} veces"
    await message.channel.send("Lista de funados:"+"```"+ mensaje + "```")

  
  elif message.content.startswith ('!funahelp'):
    await message.channel.send("Para funar a alguien ingresa el comando !funa y luego etiqueta al funado, tambien puedes usar el comando !funados para ver una lista de todos los funados")
  #Si el mensaje empieza por "!funa", guarda la id del mencionado en el mensaje y el autor del mensaje, agrega una funa con el metodo agregarFuna(), luego formatea el nombre del funado para despues mostrarlo como mensaje en el chat
  elif message.content.startswith('!funa'):
    funadoId = message.mentions[0].id
    funadorName = message.author.name
    print(funadoId, funadorName)
    agregarFuna(str(funadoId))
    print(f'{funadorName} ha funado a {await funadoName(funadoId)} ')
    if funadorName == funadoName(funadoId):
      await message.channel.send(f'```¡{funadorName} está tan confuso que se ha funado a si mismo!\n\n¡{await funadoName(funadoId)} lleva {db.get(str(funadoId))} funas!```')
    else:
      await message.channel.send(f'```¡{funadorName} ha funado a {await funadoName(funadoId)}!\n\n¡{await funadoName(funadoId)} lleva {db.get(str(funadoId))} funas!```')



client.run(my_secret)