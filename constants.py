PREFIX = "!"

# Prompts to Mistral API
QUIZ_PROMPT = "Generate a short 5-question multiple-choice quiz on {0}. \
               Each question should have 4 options (A, B, C, D) and do not include \
               the correct answers in the output."

QUIZ_DECK_PROMPT = "Generate a short 5-question multiple-choice quiz given the following question-answer prompts. \
                    If there are more than 5 question-answer prompts, randomly select 5 of them to use as a  \
                    starting point for generating the 5-question multiple chice quiz. {0}"

QUIZ_DECK_TOPIC_PROMPT = "Generate a short 5-question multiple-choice quiz on {0} given the following question-answer prompts. \
                          If there are more than 5 question-answer prompts, randomly select 5 of them to use as a  \
                          starting point for generating the 5-question multiple chice quiz. {1}"

QUIZ_TOPIC_PROMPT = "Here is a 5 question quiz:\n {0}. What is the topic \
                    of this quiz? Please just respond with your answer and no other information. \
                    For example, a quiz on the topic of whales should result in the response 'Whales'."


QUIZ_ANSWERS_PROMPT = "Here is a 5 question quiz:\n {0}. Please write a two sentence explanation \
                    of each answer. At the end of the response, please write out the answers EXACTLY in the \
                    following form: 1) A\n2) B\n.... Please think carefully about your answers and \
                    double check that the answers and your reasoning is correct but ensure that your \
                    output is not that long. Your response MUST not exceed 2000 characters."

QUIZ_HINT_PROMPT = "You are helping a student working the on the following question: {0}\n\n Please \
                    give the student a small hint that does NOT directly tell or include the answer."

CLEANED_QUIZ_ANSWERS_PROMPT = "Here are the answers to a 5 question quiz:\n\n {0}\n\n Please respond with a comma \
                               separated list of the answers to the 5 questions and no additional information.\
                               The answer should be in the form 'A,A,B,B,C'. Make SURE that the answers in \
                               the list are the exact same as in the provided answer."

GET_QUESTION_PROMPT = "Retrieve the {0}th question from the following quiz. ONLY include the question and answer choices in \
                       your response and do not include the answer. Make sure the questions are in a properly formatted bulleted list. \
                       Here is the quiz:\n\n{1}"

# Responses from our bt 
INTERACTIVE_QUIZ_FINISH = "🎉Congrats on finishing an interactive quiz session!🎉\n \
                        - Your current pig is {0} \n \
                        - Your quiz score is: **{1}%**. The correct answers were {2}.\n - Your cumulative Study Score: **{3} XP** \n \
                        - You've answered {4} questions in total - amazing! \n - Out of these questions, you got {5} correct. Keep up the great progress!"