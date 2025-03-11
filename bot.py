import os
import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv
from agent import MistralAgent
from utils import CustomHelpCommand, Quizzes

PREFIX = "!"

# Setup logging
logger = logging.getLogger("discord")

# Load the environment variables
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=CustomHelpCommand())

mistral_agent = MistralAgent()

token = os.getenv("DISCORD_TOKEN")

quiz_agent = Quizzes() 

# quizlet decks upload
class QuizData:
    def __init__(self):
        self.quiz_decks = []
        

@bot.event
async def on_ready():
    """
    Called when the client is done preparing the data received from Discord.
    Prints message on terminal when bot successfully connects to discord.

    https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
    """
    logger.info(f"{bot.user} has connected to Discord!")


@bot.event
async def on_message(message: discord.Message):
    """
    Called when a message is sent in any channel the bot can see.

    https://discordpy.readthedocs.io/en/latest/api.html#discord.on_message
    """
    # Don't delete this line! It's necessary for the bot to process commands.
    await bot.process_commands(message)

    # Ignore messages from self or other bots to prevent infinite loops.
    if message.author.bot or message.content.startswith("!"):
        return

    logger.info(f"Processing message from {message.author}: {message.content}")
    response = await mistral_agent.run(message)

    # Send the response back to the channel
    await message.reply(response)

# Command: Generate a quiz
@bot.command(name="quiz",help="Create a 5-question multiple choice quiz on any topic.")
async def generate_quiz(ctx, *, prompt=None):
    # Generate quiz on prompt
    prompt = f"Generate a short 5-question multiple-choice quiz on {prompt}. Each question should have 4 options (A, B, C, D) and do not include the correct answers in the output."
    quiz = await mistral_agent.run(prompt)
    
    # Generate topic from quiz
    quiz_topic_prompt = f"Here is a 5 question quiz:\n {quiz}. What is the topic of this quiz? Please just respond with your answer and no other information. For example, a quiz on the topic of whales should res"
    topic = await mistral_agent.run(quiz_topic_prompt)

    # Generate answers for quiz
    quiz_answers_prompt = f"Here is a 5 question quiz:\n {quiz}. Please write out the answers in the following form: 1) A - explanation\n2) B - explanation\n.... Please think carefully about your answers \
        and double check that the answers and your reasoning is correct."
    answers = await mistral_agent.run(quiz_answers_prompt)

    quiz_agent.add_quiz(quiz, topic, answers)
    await ctx.send(f"📚 **Quiz on {topic}:**\n{quiz}")

@bot.command(name="answers")
async def get_answers(ctx, *, quiz_id=None):
    """
    Get the answers to the quiz given the quiz id.
    If no quiz ID is specified, the answers to the latest quiz are returned.
    """
    # If no quiz id is specified, give answers to latest quiz
    await ctx.send(f"📚 **Quiz on {quiz_agent.get_topic_for()}:**\n{quiz_agent.get_answers_for()}")


# Check person's answers
@bot.command(name="submit_answers")
async def submit_answers(ctx, *, user_answers: str, quiz_id):
    """
    Submit your answers to the quiz in following format: !submit_answers 1A 2B 3C 4D 5A.
    The bot evaluates their performance and gives feedback.
    """

    correct_answers = quiz_agent.get_answers_for()
    user_answers_list = user_answers.split()  

    score = 0
    incorrect_questions = []

    for i, answer in enumerate(user_answers_list):
        question_num = i + 1
        correct_answer = correct_answers[i].split(") ")[1] 
        user_answer = answer[1:] 

        if user_answer.upper() == correct_answer.upper():
            score += 1
        else:
            incorrect_questions.append(f"WRONG! Question {question_num}: Correct answer was {correct_answer}, you chose {user_answer}")

    total_questions = len(correct_answers)
    feedback = f"You scored {score}/{total_questions}!\n\n"

    if incorrect_questions:
        feedback += "**Areas to Review:**\n" + "\n".join(incorrect_questions)

    await ctx.send(feedback)

'''
@bot.command(name="flashcards")
async def make_quiz_from_flashcards(ctx, *, user_answers: str):
'''


# Helper commands

# Upload quizlet slide deck
@bot.command(name="upload", help = "Upload quizlet slide deck")
async def upload_deck(ctx):
    if not ctx.message.attachments:
        await ctx.send("Please upload a .txt file with the command.")
        return
    
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(".txt"):
        await ctx.send("Only .txt files are supported for decks.")
        return
    
    content = await attachment.read()
    text = content.decode("utf-8").strip()
    
    lines = text.split("\n")
    qa_list = []
    
    for line in lines:
        parts = line.split("\t")  # Split by tab character
        if len(parts) == 2:
            question, answer = parts
            qa_list.append(f"question: {question.strip()}, answer: {answer.strip()}")
    
    response = "\n".join(qa_list) if qa_list else "No valid entries found."
    await ctx.send(f"Processed Questions and Answers:\n {response}")


# This example command is here to show you how to add commands to the bot.
# Run !ping with any number of arguments to see the command in action.
# Feel free to delete this if your project will not need commands.
@bot.command(name="ping", help="Pings the bot.")
async def ping(ctx, *, arg=None):
    if arg is None:
        await ctx.send("Pong!")
    else:
        await ctx.send(f"Pong! Your argument was {arg}")

# Start the bot, connecting it to the gateway
bot.run(token)


