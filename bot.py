import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token del bot desde las variables de entorno
TOKEN = os.getenv('DISCORD_TOKEN')

# Definir IDs de roles
ROL_APROBADO_ID_1 =   # ID del primer rol de "Aprobado"
ROL_APROBADO_ID_2 =   # ID del segundo rol de "Aprobado"
ROL_SUSPENSO_ID =     # ID del rol "Suspendido"
ROL_EJECUTOR_ID =     # ID del rol que puede ejecutar los comandos

# Definir intents
intents = discord.Intents.all()
intents.messages = True        # Habilitar el manejo de mensajes
intents.guilds = True          # Habilitar el manejo de servidores/guilds
intents.members = True         # Habilitar el manejo de miembros (incluyendo menciones de miembros)
intents.reactions = True       # Habilitar el manejo de reacciones
client = commands.Bot(command_prefix='!', intents=intents)
# Evento cuando el bot se conecta
# Evento cuando el bot se conecta
@client.event
async def on_ready():
    print(f'Bot is ready. Logged in as {client.user}')

# Comando !suspenso
@client.command()
async def suspenso(ctx, member: discord.Member):
    # Verificar si el autor del mensaje tiene el rol de ejecutor
    if discord.utils.get(ctx.author.roles, id=ROL_EJECUTOR_ID) is None:
        await ctx.send("No tienes permiso para ejecutar este comando.")
        return
    
    # Verificar si el usuario ya tiene el rol de suspendido
    if discord.utils.get(member.roles, id=ROL_SUSPENSO_ID) is not None:
        await ctx.send(f'{member.mention} ya tiene el rol de suspendido.')
        return
    
    # Añadir el rol de suspendido al usuario mencionado
    try:
        await member.add_roles(discord.Object(id=ROL_SUSPENSO_ID))
        
        # Crear un embed para el mensaje de suspensión
        embed = discord.Embed(title="Whitelist - Resultado del Examen",
                              description=f"Tras realizar tu examen Whitelist queda 💢 INSUFICIENTE 💢",
                              color=discord.Color.red())
        
        embed.add_field(name="", value=f"{member.mention}, no has superado el proceso Whitelist.\nEs tu turno de revisar las normativas de nuevo e intentarlo cuanto antes.\n¡Suerte a la próxima!")
        
        # Enviar el embed como mensaje
        await ctx.send(embed=embed)
    
    except discord.HTTPException:
        await ctx.send(f'No se pudo añadir el rol de suspendido a {member.mention}. Verifica los permisos del bot.')
    
    # Borrar el mensaje que invoca el comando
    await ctx.message.delete()

# Comando !aprobado
@client.command()
async def aprobado(ctx, member: discord.Member):
    # Verificar si el autor del mensaje tiene el rol de ejecutor
    if discord.utils.get(ctx.author.roles, id=ROL_EJECUTOR_ID) is None:
        await ctx.send("No tienes permiso para ejecutar este comando.")
        return
    
    # Verificar si el usuario ya tiene ambos roles de aprobado
    if discord.utils.get(member.roles, id=ROL_APROBADO_ID_1) is not None and discord.utils.get(member.roles, id=ROL_APROBADO_ID_2) is not None:
        await ctx.send(f'{member.mention} ya tiene ambos roles de aprobado.')
        return
    
    # Añadir ambos roles de aprobado al usuario mencionado
    try:
        await member.add_roles(discord.Object(id=ROL_APROBADO_ID_1))
        await member.add_roles(discord.Object(id=ROL_APROBADO_ID_2))
        
        # Crear un embed para el mensaje de aprobación
        embed = discord.Embed(title="Whitelist - Resultado del Examen",
                              description=f"Tras realizar tu examen Whitelist queda ✅ APROBADO ✅",
                              color=discord.Color.green())
        
        embed.add_field(name="", value=f"Bienvenido {member.mention} a la experiencia de rol en Strix Community.\nEs tu turno de disfrutar del servidor.")
        
        # Enviar el embed como mensaje
        await ctx.send(embed=embed)
    
    except discord.HTTPException:
        await ctx.send(f'No se pudo añadir ambos roles de aprobado a {member.mention}. Verifica los permisos del bot.')
    
    # Borrar el mensaje que invoca el comando
    await ctx.message.delete()

# Ejecutar el bot con el token proporcionado
client.run(TOKEN)
