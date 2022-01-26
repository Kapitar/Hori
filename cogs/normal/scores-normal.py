import disnake
from disnake.ext import commands
from disnake.ext.commands import Context

import api.scores as scores


class Scores(commands.Cog, name="scores-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="rs",
        description="Returning the most recent score for user.",
    )
    @commands.has_permissions(kick_members=True)
    async def rs(self, context: Context) -> None:
        """
        Return user's recent scores
        :param context: The context in which the command has been executed.
        """

        await scores.get_recent_score(12326522, "osu", 1)
        embed = disnake.Embed(
            title="Ass",
            description="ass",
            color=0xE02B2B
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Scores(bot))
