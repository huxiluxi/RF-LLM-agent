#LLM model
from openai import OpenAI
from prompt_toolkit.shortcuts import PromptSession

#Run LLM generated code
import subprocess

#Load prompt and results
import numpy as np
import os

#Show LLM progress
import threading
import time
import sys

session = PromptSession(multiline=True)
client = OpenAI()

def thinking_indicator(stop_event, start_time):
    spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    i = 0
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        sys.stdout.write(
            f"\r🤖 Thinking {spinner[i % len(spinner)]}  ({elapsed:.1f}s)"
        )
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    # Clear the line
    sys.stdout.write("\r" + " " * 70 + "\r")
    sys.stdout.flush()

class DesignAgent:
    def __init__(self, system_prompt, client):
        self.client = client
        self.client = client
        self.messages = [{"role": "system", "content": system_prompt}]
    
    def ask(self, text):
        self.messages.append({"role": "user", "content": text})
        response = self.client.chat.completions.create(
            model="gpt-5-mini",
            messages=self.messages,
        )
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply

# Load system prompt
with open("RF EDA Promt (Python).txt", "r", encoding="utf-8") as f:
    agentPrompt = f.read()

agent = DesignAgent(agentPrompt, client)
print("Design agent ready! Type your message. Type 'exit' to quit.\n")

design_complete = False
script_filename = "generate_patch_antenna.py"

while True:
    # End agent
    user_input = session.prompt("You:\n")
    if user_input.strip().lower() == "exit":
        print("Goodbye!")
        break

    # LLM call with spinner
    stop_event = threading.Event()
    start_time = time.time()

    t = threading.Thread(
        target=thinking_indicator,
        args=(stop_event, start_time),
        daemon=True,
    )
    t.start()

    assistant_reply = agent.ask(user_input)

    stop_event.set()
    t.join()

    elapsed = time.time() - start_time
    print(f"🤖 Thought for {elapsed:.2f} seconds\n")

    print("Assistant:\n", assistant_reply, "\n")

    # Check if the agent indicates the design/code is complete
    if "import cst_python_api as cpa" in assistant_reply:
        design_complete = True

    if design_complete:
        # Extract code block from assistant reply
        code_text = assistant_reply

        # Save generated script
        with open(script_filename, "w", encoding="utf-8") as f:
            f.write(code_text)

        print(f"Executing generated CST script: {script_filename}")
        try:
            subprocess.run(["python", script_filename], check=True)
        except subprocess.CalledProcessError as e:
            print("Error running CST script:", e)
            continue

        # Load S11 results
        if os.path.exists("S11_results.csv"):
            s11_data = np.loadtxt("S11_results.csv", delimiter=",", skiprows=1)
            freqs = s11_data[:, 0]
            S11 = s11_data[:, 1]
            
            indexMin = np.argmin(S11)

            # Send feedback to agent for optimization
            feedback_msg = f"S11 simulation (magnitude dB). Minimum at {freqs[indexMin]} GHz, with {S11[indexMin]} dB"
            
            # Optimization LLM call with spinner
            stop_event = threading.Event()
            start_time = time.time()

            t = threading.Thread(
                target=thinking_indicator,
                args=(stop_event, start_time),
                daemon=True,
            )
            t.start()

            optimization_advice = agent.ask(feedback_msg)

            stop_event.set()
            t.join()

            elapsed = time.time() - start_time
            print(f"🤖 Thought for {elapsed:.2f} seconds\n")

            print("Optimization advice:\n", optimization_advice, "\n")

        else:
            print("S11 results not found. Ensure 'S11_results.csv' exists.")
        
        # Reset design_complete if further optimization is expected
        design_complete = False
