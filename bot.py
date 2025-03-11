import os
import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv
from agent import MistralAgent

from utils import CustomHelpCommand, Quiz, QuizUpload, XPCounter
from constants import PREFIX, QUIZ_PROMPT, QUIZ_TOPIC_PROMPT, \
                        QUIZ_ANSWERS_PROMPT, QUIZ_DECK_PROMPT, \
                        INTERACTIVE_QUIZ_FINISH, CLEANED_QUIZ_ANSWERS_PROMPT, \
                        QUIZ_DECK_TOPIC_PROMPT, GET_QUESTION_PROMPT

# Setup logging
logger = logging.getLogger("discord")

# Load the environment variables
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=CustomHelpCommand())

mistral_agent = MistralAgent()

token = os.getenv("DISCORD_TOKEN")

quiz_agent = Quiz() 
quiz_upload = QuizUpload()
xp_counter = XPCounter()

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

    # Ignore non-command messages
    return


# Generate a quiz
async def generate_new_quiz(prompt):
    """
    Create a 5-question multiple choice quiz on any topic.
    """
    # Zero the score out
    quiz_agent.score = 0
    
    # Generate the quiz
    if len(quiz_upload.quiz_deck) != 0:
        if prompt is None:
            # Generate quiz from provided deck
            quiz = await mistral_agent.run(QUIZ_DECK_PROMPT.format(quiz_upload.get_deck()))
        else:
            # Generate quiz from deck and prompt
            quiz = await mistral_agent.run(QUIZ_DECK_TOPIC_PROMPT.format(prompt, quiz_upload.get_last_deck()))
    else:
        # Generate quiz from prompt
        quiz = await mistral_agent.run(QUIZ_PROMPT.format(prompt))
        
    # Generate topic from quiz
    topic = await mistral_agent.run(QUIZ_TOPIC_PROMPT.format(quiz))

    # Generate answers for quiz
    answers = await mistral_agent.run(QUIZ_ANSWERS_PROMPT.format(quiz))

    # Generate cleaned answers
    cleaned_answers_str = await mistral_agent.run(CLEANED_QUIZ_ANSWERS_PROMPT.format(answers))

    quiz_agent.add_quiz(quiz, topic, answers, list(cleaned_answers_str.split(',')))

@bot.command(name="answers")
async def get_answers(ctx):
    """
    Get the answers to the quiz given the quiz id.
    If no quiz ID is specified, the answers to the latest quiz are returned.
    """
    # If no quiz id is specified, give answers to latest quiz
    await ctx.send(f"📚 **Quiz on {quiz_agent.get_topic()}:**\n{quiz_agent.get_answers()}")

# asks the next question and checks  it
async def ask_next_question(ctx, i):
    question = await mistral_agent.run(GET_QUESTION_PROMPT.format(str(i + 1), quiz_agent.quiz))
    await ctx.send(question)

    # Ensure that user input is valid
    answer = ''
    while answer.lower() not in ['a', 'b', 'c', 'd']:
        try:
            response = await bot.wait_for("message")
            answer = response.content.strip()
        except:
            print("Too slow!")
         
    real_answers = quiz_agent.cleaned_answers
    if answer.lower() == real_answers[i].lower():
        quiz_agent.score += 1

    xp_counter.question_finish(answer == real_answers[i])
    
@bot.command(name="quiz")
async def start_quiz(ctx, *, prompt=None):
    """
    Generates a quiz in an interactive format, one question at a time. 
    """

    await generate_new_quiz(prompt)

    topic = quiz_agent.get_topic()
    await ctx.send(f"📚 **Starting Interactive Quiz on {topic}...**\n")
    for i in range(len(quiz_agent.cleaned_answers)):
        await ask_next_question(ctx, i)
    final_score = (quiz_agent.score / len(quiz_agent.cleaned_answers)) * 100 

    xp_counter.quiz_finish()
    await ctx.send(INTERACTIVE_QUIZ_FINISH.format(final_score, quiz_agent.cleaned_answers, xp_counter.xp, 
                                                  xp_counter.questions_answered, xp_counter.questions_correct))

# Upload quizlet slide deck
@bot.command(name="upload")
async def upload_deck(ctx):
    """
    Upload quizlet slide deck
    """
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
    qa_dict = {}
    
    for line in lines:
        parts = line.split("\t") 
        if len(parts) == 2:
            question, answer = parts
            qa_dict[question.strip()] = answer.strip()
    
    quiz_upload.add_new_deck(qa_dict)
    await ctx.send("Processed Questions and Answers")


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


