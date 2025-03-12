import discord
from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        """Handles the help message for the entire bot (all commands)."""
        embed = discord.Embed(
            title="QuizBot Commands",
            description="Here is a list of all available commands:",
            color=discord.Color.blue()
        )

        for command in self.context.bot.commands:
            embed.add_field(
                name=f"`{self.context.prefix}{command.name}`",
                value=command.help or "No description provided.",
                inline=False
            )

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        """Handles the help message for a single command, e.g. !help ping."""
        embed = discord.Embed(
            title=f"Help: {command.name}",
            description=command.help or "No description provided.",
            color=discord.Color.blue()
        )

        # Usage example: "!ping"
        if command.usage:
            embed.add_field(name="Usage", value=f"`{self.context.prefix}{command.name} {command.usage}`", inline=False)
        else:
            embed.add_field(name="Usage", value=f"`{self.context.prefix}{command.name}`", inline=False)

        # Aliases
        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


#  Quiz agent
class Quiz: 
    def __init__(self):
        self.last_asked = ''

    # Register that a new quiz has been created
    def add_quiz(self, quiz, topic, answers, cleaned_answers: list[str]):
        self.quiz = quiz
        self.topic = topic
        self.answers = answers
        self.cleaned_answers = cleaned_answers
        self.score = 0
        self.last_asked = ''

    def get_quiz(self):
        return self.quiz
    
    def get_topic(self):
        return self.topic
    
    def get_answers(self):
        return self.answers
    
    def get_score(self):
        return self.score

class QuizUpload:
    # quizlet decks upload
    def __init__(self):
        self.quiz_deck = {}

    def add_new_deck(self, new_deck):
        self.quiz_deck = new_deck
    
    def get_deck(self):
        """
        Format last deck as a string
        """
        return "\n".join([f"question prompt: {key}, answer: {value}" for key, value in self.quiz_deck.items()])


class XPCounter():
    def __init__(self):
        self.xp = 0
        self.interactive_quizzes_completed = 0
        self.questions_answered = 0
        self.questions_correct = 0
        self.questions_wrong = 0
        self.pig = '🐖'

        
    def question_finish(self, is_correct):
        if is_correct:
            self.questions_correct += 1
            self.xp += 1
        else:
            self.questions_wrong += 1
    
        self.questions_answered += 1
        
    async def quiz_finish(self, ctx, score):
        self.interactive_quizzes_completed += 1
        self.xp += 2

        # See whether message should be sent to user for reaching new level
        score_cutoffs = [3, 7, 15, 25]
        messages = ['1', '2', '3', '4']
        pigs = ['🐷ྀི', '₍ᐢ･⚇･ᐢ₎', 'ʚ₍՞ •̀ Ꙫ •́ ՞₎ɞ', '⍝◜ᐢ•⚇•ᐢ◝⍝']
        for i, cutoff in reversed(list(enumerate(score_cutoffs))):
            if self.xp >= cutoff and (self.xp - score - 2) < cutoff:
                await ctx.send(f"🎉Congrats‼️🎊 You have now reached StudyTier {messages[i]}. You've unlocked a new pig: {pigs[i]}.")
                return

