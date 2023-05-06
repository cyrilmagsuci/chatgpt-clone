import os
import openai
import gradio as gr
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Set the OpenAI API key using the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

# Initialize messages_array with a system message
messages_array = [
    {"role": "system", "content": "You are a helpful assistant."},
]


def openai_create(prompt):
    # Append the prompt at the end of messages_array
    messages_array.append({"role": "user", "content": prompt})

    MODEL = "gpt-3.5-turbo"

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages_array,
            temperature=0,
        )

        # Append the AI's response to the messages_array
        messages_array.append({"role": "assistant", "content": response.choices[0].message.content})

        return response.choices[0].message.content

    except Exception as e:
        error_message = f"Error: {e}"
        messages_array.append({"role": "assistant", "content": error_message})
        return error_message


def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))

    # Clear the textarea
    message.text = ""

    return history, history


block = gr.Blocks()

with block:
    gr.Markdown("""<h1><center>Build Yo'own ChatGPT with OpenAI API & Gradio</center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

block.launch(debug=True)
