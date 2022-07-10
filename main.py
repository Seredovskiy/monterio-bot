import discord
from discord.ext import commands
from config import settings


bot = commands.Bot(command_prefix = settings['PREFIX'])
bot.remove_command('help')

connection = sqlite3.connect('money.db')
cursor = connection.cursor()



@bot.event
async def on_ready():
	cursor.execute("""
		name TEXT,
		id INT,
		cash BIGINT,
		rep INT,
		lvl INT
	""")
	connection.commit()
	for guild in client.guilds:
		for member in guild.members:
			if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0)")
				connection.commit()
			else:
				pass
	print("Sussefully logged in as {0.user}".format(bot))
	print("The prefix of bot is: $")
	await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.watching, name = "Server Rules"))

@bot.event
async def on_member_join(member):
	if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
		cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0)")
	else:
		pass

@bot.command()
async def test(ctx):
	await ctx.send("ura!")
@bot.command()
async def ping(ctx):
	await ctx.send("pong!")
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = None):
	if reason == None:
		reason = "No reason provided!"
		await ctx.send(reason)
	await ctx.guild.kick(member)
	await ctx.send(f"User {member.mention} has been kicked for: {reason}!")

@kick.error
async def kick_error(error, ctx):
	if isinstance(error, MissingPermissions):
		text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
		await bot.send_message(ctx.message.channel, text)

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
	if reason == None:
		reason = "No reason provided!"
		await ctx.send(reason)
	await ctx.guild.ban(member)
	await ctx.send(f"User {member.mention} has been banned for: {reason}!")

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, member: discord.Member, *, reason = None):
	if reason == None:
		reason = "No reason provided!"
		await ctx.send(reason)
	await ctx.guild.unban(member)
	await ctx.send(f"User {member.mention} has been banned for: {reason}!")


#---------------------------------------------------------------------------------


bot.run(settings['TOKEN'])