import wyvern
from wyvern import commands

client = wyvern.CommandsClient("TOKEN")


@client.with_slash_command(name="ping", description="sends a pong response.")
async def ping(interaction: wyvern.AppCommandInter) -> None:
    await interaction.create_message_response("pong!")


@commands.with_option(name="text", description="the text to send.")
@client.with_slash_command(name="echo", description="repeats your text.")
async def echo(interaction: wyvern.AppCommandInter, text: str) -> None:
    await interaction.create_message_response(text)

client.run()
