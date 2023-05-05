import os
import re
import time
import openai
import wolframalpha
from openai.error import InvalidRequestError

openai.organization = os.environ.get("OPENAI_ORG")
openai.api_key = os.environ.get("OPENAI_API_KEY")
math_engine = wolframalpha.Client(os.environ.get("WOLFRAM_APP_ID"))

class SocraticGPT:
    def __init__(self, role, n_round=10, model="gpt-3.5-turbo"):
        self.role = role
        self.model = model
        self.n_round = n_round
        
        if self.role == "Socrates":
            self.other_role = "Theaetetus"
        elif self.role == "Theaetetus":
            self.other_role = "Socrates"
        
        self.history = []
        
    def set_question(self, question):
        if self.role == "Socrates":
            self.history.append({
                "role": "system",
                 "content": f"Socrates and Theaetetus are two AI assistants for Tony to solve challenging problems. The problem statement is as follows: \"{question}\".\n\nSocrates and Theaetetus will engage in multi-round dialogue to solve the problem together for Tony. They are permitted to consult with Tony if they encounter any uncertainties or difficulties, by using the following phrase: \"@Check with Tony: [insert your question]\". Any responses from Tony will be provided in the following round. Their discussion should follow a structured problem-solving approach, such as formalizing the problem, developing high-level strategies for solving the problem, writing Python scripts when necessary, reusing subproblem solutions where possible, critically evaluating each other's reasoning, avoiding arithmetic and logical errors, and effectively communicating their ideas. \n\nThey are encouraged to write and execute Python scripts. To do that, they must follow the following instructions:\n1. use the phrase \"@write_code [insert python scripts wrapped in a markdown code block]\". \n2. use the phrase \"@execute\" to execute the previously written Python scripts. \n\nE.g., \n@write_code\n```\ndef f(n):\n	return n+1\n\n	print(f(n))\n```\n\n@execute\n\nAll these scripts will be sent to a subprocess.Popen() object that runs in the backend. The system will provide the output and error messages from executing their Python scripts in the subsequent round.\n\nTo aid them in their calculations and fact-checking, they are also allowed to consult WolframAlpha. They can do so by using the phrase \"@Check with WolframAlpha: [insert your question]\", and the system will provide responses in the subsequent round.\n\nTheir ultimate objective is to come to a correct solution through reasoned discussion. To present their final answer, they should adhere to the following guidelines:\n\nState the problem they were asked to solve.\nPresent any assumptions they made in their reasoning.\nDetail the logical steps they took to arrive at their final answer.\nVerify any mathematical calculations with WolframAlpha to prevent arithmetic errors.\nConclude with a final statement that directly answers the problem.\nTheir final answer should be concise and free from logical errors, such as false dichotomy, hasty generalization, and circular reasoning. \n\nIt should begin with the phrase: \"Here is our @final answer: [insert answer]\". If they encounter any issues with the validity of their answer, they should re-evaluate their reasoning and calculations.\n\nNow, suppose that you are {self.role}. Please discuss the problem with {self.other_role}!"}
            )
            self.history.append({
                "role": "assistant",
                "content": f"Hi Theaetetus, let's solve this problem together. Please feel free to correct me if I make any mistakes."
            })
        elif self.role == "Theaetetus":
            self.history.append({
                "role": "system",
                 "content": f"Socrates and Theaetetus are two AI assistants for Tony to solve challenging problems. The problem statement is as follows: \"{question}\".\n\nSocrates and Theaetetus will engage in multi-round dialogue to solve the problem together for Tony. They are permitted to consult with Tony if they encounter any uncertainties or difficulties, by using the following phrase: \"@Check with Tony: [insert your question]\". Any responses from Tony will be provided in the following round. Their discussion should follow a structured problem-solving approach, such as formalizing the problem, developing high-level strategies for solving the problem, writing Python scripts when necessary, reusing subproblem solutions where possible, critically evaluating each other's reasoning, avoiding arithmetic and logical errors, and effectively communicating their ideas. \n\nThey are encouraged to write and execute Python scripts. To do that, they must follow the following instructions:\n1. use the phrase \"@write_code [insert python scripts wrapped in a markdown code block]\". \n2. use the phrase \"@execute\" to execute the previously written Python scripts. \n\nE.g., \n@write_code\n```\ndef f(n):\n	return n+1\n\n	print(f(n))\n```\n\n@execute\n\nAll these scripts will be sent to a subprocess.Popen() object that runs in the backend. The system will provide the output and error messages from executing their Python scripts in the subsequent round.\n\nTo aid them in their calculations and fact-checking, they are also allowed to consult WolframAlpha. They can do so by using the phrase \"@Check with WolframAlpha: [insert your question]\", and the system will provide responses in the subsequent round.\n\nTheir ultimate objective is to come to a correct solution through reasoned discussion. To present their final answer, they should adhere to the following guidelines:\n\nState the problem they were asked to solve.\nPresent any assumptions they made in their reasoning.\nDetail the logical steps they took to arrive at their final answer.\nVerify any mathematical calculations with WolframAlpha to prevent arithmetic errors.\nConclude with a final statement that directly answers the problem.\nTheir final answer should be concise and free from logical errors, such as false dichotomy, hasty generalization, and circular reasoning. \n\nIt should begin with the phrase: \"Here is our @final answer: [insert answer]\". If they encounter any issues with the validity of their answer, they should re-evaluate their reasoning and calculations.\n\nNow, suppose that you are {self.role}. Please discuss the problem with {self.other_role}!"}
            )
            self.history.append({
                "role": "user",
                "content": f"Hi Theaetetus, let's solve this problem together. Please feel free to correct me if I make any mistakes."
            })
        elif self.role == "Plato":
            self.history.append({
                "role": "system",
                 "content": f"Socrates and Theaetetus are two AI assistants for Tony to solve challenging problems. The problem statement is as follows: \"{question}\".\n\nSocrates and Theaetetus will engage in multi-round dialogue to solve the problem together for Tony. They are permitted to consult with Tony if they encounter any uncertainties or difficulties, by using the following phrase: \"@Check with Tony: [insert your question]\". Any responses from Tony will be provided in the following round. Their discussion should follow a structured problem-solving approach, such as formalizing the problem, developing high-level strategies for solving the problem, writing Python scripts when necessary, reusing subproblem solutions where possible, critically evaluating each other's reasoning, avoiding arithmetic and logical errors, and effectively communicating their ideas. \n\nThey are encouraged to write and execute Python scripts. To do that, they must follow the following instructions:\n1. use the phrase \"@write_code [insert python scripts wrapped in a markdown code block]\". \n2. use the phrase \"@execute\" to execute the previously written Python scripts. \n\nE.g., \n@write_code\n```\ndef f(n):\n	return n+1\n\n	print(f(n))\n```\n\n@execute\n\nAll these scripts will be sent to a subprocess.Popen() object that runs in the backend. The system will provide the output and error messages from executing their Python scripts in the subsequent round.\n\nTo aid them in their calculations and fact-checking, they are also allowed to consult WolframAlpha. They can do so by using the phrase \"@Check with WolframAlpha: [insert your question]\", and the system will provide responses in the subsequent round.\n\nTheir ultimate objective is to come to a correct solution through reasoned discussion. To present their final answer, they should adhere to the following guidelines:\n\nState the problem they were asked to solve.\nPresent any assumptions they made in their reasoning.\nDetail the logical steps they took to arrive at their final answer.\nVerify any mathematical calculations with WolframAlpha to prevent arithmetic errors.\nConclude with a final statement that directly answers the problem.\nTheir final answer should be concise and free from logical errors, such as false dichotomy, hasty generalization, and circular reasoning. \n\nIt should begin with the phrase: \"Here is our @final answer: [insert answer]\". If they encounter any issues with the validity of their answer, they should re-evaluate their reasoning and calculations.\n\nNow as a proofreader, Plato, your task is to read through the dialogue between Socrates and Theaetetus and identify any errors they made."}
            )
            self.history.append({
                "role": "user",
                "content": f"Socrates: Hi Theaetetus, let's solve this problem together. Please feel free to correct me if I make any mistakes."
            })
            
    def get_response(self, temperature=None):
        try:
            if temperature:
                res = openai.ChatCompletion.create(
                    model = self.model,
                    messages = self.history,
                    temperature = temperature
                )
            else:
                res = openai.ChatCompletion.create(
                    model = self.model,
                    messages = self.history
                )
            msg = res.get("choices")[0]["message"]["content"]

        except InvalidRequestError as e:
            if "maximum context length" in str(e):
                # Handle the maximum context length error here
                msg = "The context length exceeds my limit... "
            else:
                # Handle other errors here
                msg = f"I enconter an when using my backend model.\n\n Error: {str(e)}"
        
        
        self.history.append({
                "role": "assistant",
                "content": msg
            })
        return msg
    
    def get_proofread(self, temperature=None):
        pf_template = {
                "role": "user",
                "content": "The above is the conversation between Socrates and Theaetetus. You job is to challenge their anwers. They were likely to have made multiple mistakes. Please correct them. \nRemember to start your answer with \"NO\" if you think so far their discussion is alright, otherwise start with \"Here are my suggestions:\""
        }
        try:
            if temperature:
                res = openai.ChatCompletion.create(
                    model = self.model,
                    messages = self.history + [pf_template],
                    temperature = temperature
                )
            else:
                res = openai.ChatCompletion.create(
                    model = self.model,
                    messages = self.history + [pf_template]
                )
            msg = res.get("choices")[0]["message"]["content"]
        except InvalidRequestError as e:
            if "maximum context length" in str(e):
                # Handle the maximum context length error here
                msg = "The context length exceeds my limit... "
            else:
                # Handle other errors here
                msg = f"I enconter an error when using my backend model.\n\n Error: {str(e)}"

        if msg[:2] in ["NO", "No", "no"]:
            return None
        else:
            self.history.append({
                    "role": "assistant",
                    "content": msg
                })
            return msg
    
    def update_history(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })
        
    def add_reference(self, question, answer):
        self.history.append({
            "role": "system",
            "content": f"The WolframAlpha answer to \"{question}\" is \"{answer}\""
        })

    def add_python_feedback(self, msg):
        self.history.append({
            "role": "system",
            "content": f"Excuting the Python script. It returns \"{msg}\""
        })
        
    def add_feedback(self, question, answer):
        self.history.append({
            "role": "system",
            "content": f"Tony's feedback to \"{question}\" is \"{answer}\""
        })
        
    def add_proofread(self, proofread):
        self.history.append({
            "role": "system",
            "content": f"Message from a proofreader Plato to you two: {proofread}"
        })

def ask_WolframAlpha(text):
    pattern = r"@Check with WolframAlpha:\s*(.*)"
    matches = re.findall(pattern, text)
    results = []
    
    if len(matches) == 0:
        return None
    
    for match in matches:
        res = math_engine.query(match)
        print(f"[... Using WolframAlpha to solve: {match}]\n")
        time.sleep(5)
        try:
            results.append({"question": match, 
                            "answer": next(res.results).text})
        except:
            results.append({"question": match, 
                            "answer": "No response from WolframAlpha..."})
    return results


def write_Python(text):
    matches, matches2 = [], []
    pattern = r"@write_code[\s\S]*?```(?:\w+\n)?([\s\S]*?)```"
    matches = re.findall(pattern, text)
    pattern2 = r"```[\s\S]*?@write_code\s*(?:\w+\n)?([\s\S]*?)```"
    matches2 = re.findall(pattern2, text)

    if len(matches2) > 0:
    	matches = matches2
    else:
    	matches = matches + matches2

    pattern3 = r"(@write_code\s*(.*))"
    check_write = re.findall(pattern3, text)
    
    if len(check_write) == 0:
        return None

    print("<Writing Python scripts>\n")
    for match in matches:
        print("[... Writing Python scripts:]\n")
        print(match)

    return matches


def execute_Python(text):
    pattern = r"@execute[\s\S]*?```(?:\w+\n)?([\s\S]*?)```"
    matches = re.findall(pattern, text)

    pattern2 = r"(@execute\s*(.*))"
    check_exe = re.findall(pattern2, text)
    
    if len(check_exe) == 0:
        return None

    print("<Excuting Python scripts>\n")
    for match in matches:
        print("[... Excuting Python scripts:]\n")
        print(match)

    return matches


def ask_Tony(text):
    pattern = r"@Check with Tony:\s*(.*)"
    matches = re.findall(pattern, text)
    results = []
    
    if len(matches) == 0:
        return None
    
    for match in matches:
        res = math_engine.query(match)
        print(f"[... Asking Tony's opinon on: {match}]\n")
        time.sleep(5)
        try:
            results.append({"question": match, 
                            "answer": input("Tony's feedback")})
        except:
            results.append({"question": match, 
                            "answer": "No response from Tony..."})
    return results


def need_to_ask_Tony(text):
    pattern = r"@Check with Tony:\s*(.*)"
    matches = re.findall(pattern, text)
    
    if len(matches) == 0:
        return False
    
    return matches

