import ollama
import sys
import subprocess
import os
import datetime
import json

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Base Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTEN_DIR = os.path.join(BASE_DIR, "agenten")


# Global AGENTS dictionary to support dynamic updates
AGENTS = {}


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Fehler beim Lesen von {path}: {str(e)}"

def launch_aider(agent_name="General"):
    print(f"\nStarte Aider für {agent_name}... (Neues Fenster sollte sich öffnen)")
    aider_bat = os.path.join(BASE_DIR, "start_aider.bat")
    
    # Custom title for the window
    title = f"Aider - {agent_name}"
    
    try:
        # Start in new window with specific title
        subprocess.Popen(f'start "{title}" cmd /k "{aider_bat}"', shell=True)
    except Exception as e:
        print(f"Fehler beim Starten von Aider für {agent_name}: {e}")

# Tool definition for Moderator Communication
def contact_moderator(message, priority="NORMAL"):
    """
    Sends a message to the moderator (user).
    Use this when you are stuck, need a decision, or want to report completion.
    Priority: LOW, NORMAL, HIGH, CRITICAL
    """
    prefix = ""
    if priority == "CRITICAL":
        prefix = "!!! KRITISCH !!! "
    elif priority == "HIGH":
        prefix = "!!! WICHTIG !!! "
        
    print(f"\n\n{'='*40}")
    print(f"[MODERATOR-RUF] {prefix}{message}")
    print(f"{'='*40}\n")
    return "Nachricht an Moderator gesendet. Warte auf Antwort im Chat."

# Tool definition for Worker Initialization
def init_worker(name, role_file="05_worker.md"):
    """
    Initializes a new worker agent with the given name and role file.
    Example: init_worker("Frontend-Engineer", "04_Frontend-Engineer.md")
    """
    global AGENTS
    print(f"\n[SYSTEM] Initialisiere neuen Worker: {name} ({role_file})...")
    
    # Check if role file exists
    role_path = os.path.join(AGENTEN_DIR, role_file)
    if not os.path.exists(role_path):
        return f"Fehler: Rollendatei {role_file} nicht gefunden."
    
    # Create ID from name (sanitize)
    worker_id = name.lower().replace(" ", "_").replace("-", "_")
    
    # Init Agent with default tools (contact_moderator)
    # New workers don't get init_worker tool, only Architect does.
    new_agent = MistralAgent(name, worker_id, role_file, tools=[contact_moderator])
    
    # Register in Global Dict
    # Find next free key (numeric)
    existing_keys = [int(k) for k in AGENTS.keys() if k.isdigit()]
    next_key = str(max(existing_keys) + 1) if existing_keys else "3"
    
    AGENTS[next_key] = new_agent

    
    # Launch Aider
    launch_aider(name)
    
    return f"Worker {name} erfolgreich initialisiert (Key: {next_key}). Aider gestartet."

class MistralAgent:
    def __init__(self, name, id_file, role_file, tools=None):
        self.name = name
        self.id = id_file 
        self.role_file = role_file
        self.messages = []
        self.status = "BOOTING"
        self.tools = tools if tools else []
        
        # Load Instructions
        self.global_rules = read_file(os.path.join(AGENTEN_DIR, "00_agenten.md"))
        self.role_rules = read_file(os.path.join(AGENTEN_DIR, role_file))
        
        # Build System Prompt
        self.system_prompt = (
            f"Du bist der {self.name}.\n\n"
            f"=== GLOBALE REGELN ===\n{self.global_rules}\n\n"
            f"=== DEINE ROLLE ===\n{self.role_rules}\n\n"
            f"=== CODING ===\n"
            f"Du bist für das 'WAS' zuständig, Aider für das 'WIE'.\n"
            f"Code-Änderungen machst du via Aider (Anweisung an User oder eigenes Fenster).\n"
        )
        
        if self.tools:
            self.system_prompt += (
                f"\n=== TOOLS ===\n"
                f"Du hast Zugriff auf Tools. Nutze sie, wenn nötig.\n"
                f"- `contact_moderator`: Um den Moderator zu rufen (Fragen, Probleme, Fertigmeldung).\n"
            )
            # Add specific hint for Architect
            if "init_worker" in [t.__name__ for t in self.tools]:
                self.system_prompt += f"- `init_worker`: Um neue Agenten zu erstellen.\n"
        
        self.system_prompt += f"\nBeginne jede Antwort mit '{self.name}: '"
        
        # Init History
        self.messages.append({'role': 'system', 'content': self.system_prompt})

    def chat(self, user_input):
        self.messages.append({'role': 'user', 'content': user_input})
        
        print(f"\n[{self.name} denkt...]")
        
        max_retries = 3
        final_answer = ""
        
        for attempt in range(max_retries):
            # Pass tools if available
            kwargs = {'model': 'mistral', 'messages': self.messages}
            if self.tools:
                kwargs['tools'] = self.tools

            response = ollama.chat(**kwargs)
            message = response['message']
            self.messages.append(message)
            
            if message.get('tool_calls'):
                print(f"[{self.name} nutzt Tool...]")
                for tool in message['tool_calls']:
                    function_name = tool['function']['name']
                    args = tool['function']['arguments']
                    
                    result = ""
                    if function_name == 'init_worker':
                        result = init_worker(args.get('name'), args.get('role_file', '05_worker.md'))
                    elif function_name == 'contact_moderator':
                        result = contact_moderator(args.get('message'), args.get('priority', 'NORMAL'))
                    
                    print(f"Tool Result: {result}")
                        
                    self.messages.append({
                        'role': 'tool',
                        'content': result,
                    })
            else:
                final_answer = message['content']
                print(f"{self.name}: {final_answer}")
                break
        
        return final_answer

def main():
    global AGENTS
    print("=== Agent Orchestrator ===")
    print("Initialisiere Sub-Agenten...")
    
    # Init Agents
    # Product Manager has contact_moderator
    prod_man = MistralAgent("Produktmanager", "02_Produktmanager", "02_Produktmanager.md", tools=[contact_moderator])
    
    # Architekt has init_worker AND contact_moderator
    architekt = MistralAgent("Systemarchitekt", "03_Systemarchitekt", "03_Systemarchitekt.md", tools=[init_worker, contact_moderator])
    
    AGENTS["1"] = prod_man
    AGENTS["2"] = architekt

    print("\nAlle Agenten bereit.")
    
    # AUTOMATIC AIDER LAUNCH
    print("\n[System] Starte Coding-Interfaces (Aider) für Agenten...")
    launch_aider("Produktmanager")
    launch_aider("Systemarchitekt")
    

    
    while True:
        print("\n=== MENÜ ===")
        # Dynamic Menu
        for key, agent in AGENTS.items():
            print(f"{key}: Chat mit {agent.name}")
        print("q: Beenden")
        
        choice = input("\nAuswahl: ")
        
        if choice.lower() == 'q':
            break
            
        agent = AGENTS.get(choice)
        if agent:
            print(f"\n--- Chat mit {agent.name} ---")
            print("(Tippe 'z' um zum Hauptmenü zurückzukehren)")
            while True:
                msg = input(f"Nachricht an {agent.name}: ")
                if msg.lower() == 'z':
                    break
                agent.chat(msg)
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()
