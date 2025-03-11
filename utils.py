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


# Store created quizzes
class Quizzes: 
    def __init__(self):
        # self.topics = []
        # Map questions to answers
        self.quizzes = []

    # Adds a quiz, topic, and answers and returns the id
    def add_quiz(self, quiz, topic, answers):
        self.quizzes.append([quiz, topic, answers])
        return len(self.quizzes) - 1
    
    def get_answers_for(self):
        return self.get_answers_for(len(self.quizzes) - 1)

    def get_answers_for(self, id):
        return self.quizzes[id][2]
    
    def get_topic_for(self):
        return self.get_topic_for(len(self.quizzes) - 1)

    def get_topic_for(self, id):
        return self.quizzes[id][1]

    # def add_topics(self, topic):
    #     self.topics.append(topic)

    # def generate_quiz(self, quiz, answers):
    #     self.quizzes[self.quiz_id] = {} 
    #     self.quizzes[self.quiz_id][quiz] = answers
    #     self.quiz_id += 1

    # def get_last_topic(self): 
    #     return self.topics[-1]

    # def get_last_quiz(self):
    #     return self.quizzes[-1]
    
    # def get_quizzes(self):
    #     return list(self.quizzes.keys())
    
    # def get_topics(self):
    #     return self.topics
        
    # def get_answers(self):
    #     return [list(quiz.values()) for quiz in self.quizzes] 