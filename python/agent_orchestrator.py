import ollama
import sys
import subprocess
import os
import datetime
import json
import re

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Base Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTEN_DIR = os.path.join(BASE_DIR, "agenten")

# Simple .env loader
def load_env():
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
                    
load_env()
PROJECT_ROOT = os.environ.get("PROJECT_ROOT", BASE_DIR)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")

# Global AGENTS dictionary to support dynamic updates
AGENTS = {}

def read_file(path):
    try:
        # Resolve path
        if os.path.isabs(path):
            abs_path = path
        else:
            abs_path = os.path.join(PROJECT_ROOT, path)
            
        if not os.path.exists(abs_path):
             return f"Fehler: Datei nicht gefunden: {abs_path}"

        with open(abs_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Fehler beim Lesen von {path}: {str(e)}"

def write_file(path, content):
    """
    Writes content to a file.
    path: Relative path from PROJECT_ROOT (e.g. 'features/ueber-uns/02_spec.md') or absolute path.
    content: The content to write.
    """
    try:
        # Resolve path
        if os.path.isabs(path):
            abs_path = path
        else:
            abs_path = os.path.join(PROJECT_ROOT, path)
            
        # Security check: Ensure we are within PROJECT_ROOT
        # (Basic check, can be improved)
        if PROJECT_ROOT.lower() not in os.path.abspath(abs_path).lower():
             return f"Fehler: Zugriff verweigert. Pfad muss innerhalb von {PROJECT_ROOT} liegen."

        # Ensure directory exists
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f"Datei erfolgreich geschrieben: {abs_path}"
    except Exception as e:
        return f"Fehler beim Schreiben von {path}: {str(e)}"

def launch_aider(agent_name="General"):
    print(f"\nStarte Aider für {agent_name}... (Neues Fenster sollte sich öffnen)")
    aider_bat = os.path.join(BASE_DIR, "start_aider.bat")

    if not os.path.exists(aider_bat):
        print(f"[ERROR] Start-Skript nicht gefunden: {aider_bat}")
        return

    # Use helper batch file for reliable window launching
    launcher = os.path.join(BASE_DIR, "launch_window.bat")
    
    if not os.path.exists(launcher):
         print(f"[ERROR] Launcher-Skript nicht gefunden: {launcher}")
         return

    try:
        print(f"[DEBUG] Invoking launcher for {agent_name}")
        # subprocess.call is fine here because the bat file uses 'start' (non-blocking) and exits
        subprocess.call([launcher, f"Aider - {agent_name}", aider_bat])
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
    if not message:
        message = "Keine Nachricht."
        
    if priority == "CRITICAL":
        prefix = "!!! KRITISCH !!! "
    elif priority == "HIGH":
        prefix = "!!! WICHTIG !!! "
        
    print(f"\n\n{'='*40}")
    print(f"[MODERATOR-RUF] {prefix}{message}")
    print(f"{'='*40}\n")
    return "Nachricht an Moderator gesendet. Warte auf Antwort im Chat."

# Tool definition for Agent-to-Agent Communication
def send_message(recipient_name, message):
    """
    Sends a message to another agent.
    recipient_name: Name of the target agent (e.g. "Systemarchitekt", "Frontend-Engineer")
    message: The content of the message
    """
    target_agent = None
    if not recipient_name:
        return "Fehler: Kein Empfänger angegeben."
        
    for key, agent in AGENTS.items():
        if agent.name.lower() == recipient_name.lower():
            target_agent = agent
            break
            
    if target_agent:
        # We inject the message into the target agent's history as a user message
        # stating who sent it.
        sender_info = "[NACHRICHT VON EINEM ANDEREN AGENTEN]"
        full_msg = f"{sender_info}\n\n{message}"
        target_agent.messages.append({'role': 'user', 'content': full_msg})
        print(f"\n[INTERN] Nachricht an {target_agent.name} zugestellt.")
        return f"Nachricht an {target_agent.name} erfolgreich gesendet."
    else:
        return f"Fehler: Agent '{recipient_name}' nicht gefunden."

# Tool definition for Worker Initialization
def init_worker(name, role_file="05_worker.md"):
    """
    Initializes a new worker agent with the given name and role file.
    Example: init_worker("Frontend-Engineer", "04_Frontend-Engineer.md"), "04_Frontend-Engineer.md")
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
    # [CHANGE] Added read_file and write_file because we are running headless (no Aider window)
    new_agent = MistralAgent(name, worker_id, role_file, tools=[contact_moderator, send_message, read_file, write_file])
    
    # Register in Global Dict
    # Find next free key (numeric)
    existing_keys = [int(k) for k in AGENTS.keys() if k.isdigit()]
    next_key = str(max(existing_keys) + 1) if existing_keys else "3"
    
    AGENTS[next_key] = new_agent
    
    # Launch Aider
    # launch_aider(name) # DISABLED per User Request
    
    return f"Worker {name} erfolgreich initialisiert (Key: {next_key}). (Headless Mode - kein Aider Fenster)"

# State Persistence
STATE_FILE = os.path.join(BASE_DIR, "agent_state.json")

def save_state():
    """Saves the current state of all agents to JSON."""
    data = {}
    for key, agent in AGENTS.items():
        data[key] = agent.to_dict()
    
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        # print("[SYSTEM] Status gespeichert.") 
    except Exception as e:
        print(f"[ERROR] Fehler beim Speichern des Status: {e}")

def load_state():
    """Loads agents from JSON file if it exists."""
    global AGENTS
    if not os.path.exists(STATE_FILE):
        return False
        
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for key, agent_data in data.items():
            # Reconstruct agent
            # Map tool names back to functions
            tool_names = agent_data.get('tools', [])
            tools = []
            if 'contact_moderator' in tool_names: tools.append(contact_moderator)
            if 'send_message' in tool_names: tools.append(send_message)
            if 'contact_moderator' in tool_names: tools.append(contact_moderator)
            if 'send_message' in tool_names: tools.append(send_message)
            if 'init_worker' in tool_names: tools.append(init_worker)
            if 'read_file' in tool_names: tools.append(read_file)
            if 'write_file' in tool_names: tools.append(write_file)
            
            agent = MistralAgent(
                name=agent_data['name'],
                id_file=agent_data['id'],
                role_file=agent_data['role_file'],
                tools=tools
            )
            if agent_data['messages']:
                agent.messages = agent_data['messages']
            agent.status = agent_data.get('status', 'UNKNOWN')
            AGENTS[key] = agent
            
        print(f"[SYSTEM] Status geladen: {len(AGENTS)} Agenten wiederhergestellt.")
        return True
    except Exception as e:
        print(f"[ERROR] Fehler beim Laden des Status: {e}")
        return False

# Helper for JSON serialization
def make_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(v) for v in obj]
    elif hasattr(obj, 'model_dump'):
        return make_serializable(obj.model_dump())
    elif hasattr(obj, 'to_dict'):
        return make_serializable(obj.to_dict())
    elif hasattr(obj, '__dict__'):
        return make_serializable(obj.__dict__)
    else:
        return obj

def extract_tool_calls(content):
    """
    Parses content for tool calls in the Global Block Format:
    [[TOOL: tool_name]]
    [[ARG: arg1]]
    val1
    [[ARG: arg2]]
    val2
    [[END_TOOL]]
    """
    tool_calls = []
    
    # Regex to find tool blocks
    # Flags: DOTALL to match newlines
    tool_pattern = re.compile(r'\[\[TOOL:\s*(.*?)\]\](.*?)\[\[END_TOOL\]\]', re.DOTALL | re.IGNORECASE)
    blocks = tool_pattern.findall(content)
    
    for tool_name, block_content in blocks:
        tool_name = tool_name.strip()
        arguments = {}
        
        # Parse arguments within the block
        # Split by [[ARG: ... ]]
        # We need to be careful to capture the arg name and the content following it
        arg_pattern = re.compile(r'\[\[ARG:\s*(.*?)\]\]', re.IGNORECASE)
        
        # Split the content by the arg pattern
        parts = arg_pattern.split(block_content)
        
        # parts[0] is content before first arg (usually empty/whitespace)
        # parts[1] is first arg name
        # parts[2] is first arg content
        # parts[3] is second arg name
        # parts[4] is second arg content
        # ... based on re.split behavior with capturing group
        
        if len(parts) > 1:
            # Iterate starting from index 1, taking 2 items at a time
            for i in range(1, len(parts), 2):
                arg_name = parts[i].strip()
                if i + 1 < len(parts):
                    arg_value = parts[i+1].strip()
                    arguments[arg_name] = arg_value
        
        tool_calls.append({
            'function': {
                'name': tool_name,
                'arguments': arguments
            }
        })
            
    return tool_calls

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
        )
        
        self.system_prompt += (
            f"=== CODING ===\n"
            f"Du bist für das 'WAS' zuständig, Aider für das 'WIE'.\n"
            f"Code-Änderungen machst du via Aider (Anweisung an User oder eigenes Fenster).\n"
        )
        
        if self.tools:
            self.system_prompt += (
                f"\n=== TOOLS & ACTION ===\n"
                f"Du hast Zugriff auf Tools. WICHTIG: DEINE HAUPTAUFGABE IST HANDELN, NICHT REDEN.\n"
                f"Wenn du eine Aufgabe hast (z.B. eine Datei erstellen), nutze SOFORT das entsprechende Tool.\n"
                f"Beschreibe nicht, was du tun wirst. TU ES EINFACH.\n"
                f"- `contact_moderator`: Um den Moderator zu rufen (Fragen, Probleme, Fertigmeldung).\n"
                f"- `send_message`: Um Nachrichten an andere Agenten zu senden (z.B. Produktmanager an Architekt).\n"
                f"- `read_file(path)`: Liest eine Datei (Pfad relativ zu PROJECT_ROOT oder absolut).\n"
                f"- `write_file(path, content)`: Schreibt eine Datei. WICHTIG: Das Argument 'content' MUSS den VOLLSTÄNDIGEN Quellcode enthalten (HTML, CSS, JS etc.). Keine Zusammenfassungen, keine Platzhalter, keine 'Hier kommt Code hin'-Kommentare. Schreibe den kompletten, funktionierenden Code!\n"
            )
            # Add specific hint for Architect
            if "init_worker" in [t.__name__ for t in self.tools]:
                self.system_prompt += f"- `init_worker`: Um neue Agenten zu erstellen.\n"
        
        self.system_prompt += f"\nBeginne jede Antwort mit '{self.name}: '"

        # FALLBACK INSTRUCTIONS FOR MODELS WITHOUT NATIVE TOOL SUPPORT
        if self.tools:
            self.system_prompt += (
                "\n\n=== TOOL USAGE (FALLBACK) ===\n"
                "Falls native Tools nicht verfügbar sind oder du sie nicht nutzen kannst, nutze AUSSCHLIESSLICH folgendes Format:\n"
                "\n"
                "[[TOOL: tool_name]]\n"
                "[[ARG: arg_name]]\n"
                "wert_zeile_1\n"
                "wert_zeile_2\n"
                "[[ARG: arg2]]\n"
                "wert\n"
                "[[END_TOOL]]\n"
                "\n"
                "BEISPIEL FÜR `write_file`:\n"
                "[[TOOL: write_file]]\n"
                "[[ARG: path]]\n"
                "features/test/index.html\n"
                "[[ARG: content]]\n"
                "<html>\n"
                "  <body>\n"
                "    <h1>Hallo Welt!</h1>\n"
                "  </body>\n"
                "</html>\n"
                "[[END_TOOL]]\n"
                "\n"
                "WICHTIG:\n"
                "- Nutze KEIN JSON!\n"
                "- Schreibe Argumente in `[[ARG: ...]]` Blöcke.\n"
                "- Der Inhalt kann über viele Zeilen gehen.\n"
                "- Antworte NUR mit diesem Block.\n"
            )
        
        # Init History only if empty (handled by load logic mostly, but good safety)
        if not self.messages:
            self.messages.append({'role': 'system', 'content': self.system_prompt})

    def to_dict(self):
        """Serializes the agent to a dictionary."""
        return {
            'name': self.name,
            'id': self.id,
            'role_file': self.role_file,
            'messages': self.messages,
            'status': self.status,
            'tools': [t.__name__ for t in self.tools]
        }

    def chat(self, user_input):
        self.messages.append({'role': 'user', 'content': user_input})
        save_state() # Save after user input
        
        print(f"\n[{self.name} denkt...]")
        
        max_retries = 3
        final_answer = ""
        
        for attempt in range(max_retries):
            # Pass tools if available
            kwargs = {'model': OLLAMA_MODEL, 'messages': self.messages}
            if self.tools:
                kwargs['tools'] = self.tools

            try:
                # Try native tool calling first
                response = ollama.chat(**kwargs)
            except Exception as e:
                # If error is likely due to missing tool support (Status 400), try text-only
                if "does not support tools" in str(e) or "400" in str(e):
                    print(f"[{self.name}] Native Tools nicht unterstützt. Versuche Text-Modus...")
                    if 'tools' in kwargs:
                        del kwargs['tools']
                    response = ollama.chat(**kwargs)
                else:
                    raise e

            message = response['message']
            
            # Robust conversion
            message = make_serializable(message)

            self.messages.append(message)
            save_state() # Save after model response
            
            # CHECK FOR TOOLS (Native OR Extracted)
            tool_calls = message.get('tool_calls', [])
            
            # If no native tools, check for manual JSON parsing
            if not tool_calls:
                tool_calls = extract_tool_calls(message.get('content', ''))
            
            if tool_calls:
                print(f"[{self.name} nutzt Tool...]")
                for tool in tool_calls:
                    function_name = tool['function']['name']
                    args = tool['function']['arguments']
                    
                    result = ""
                    if function_name == 'init_worker':
                        result = init_worker(args.get('name'), args.get('role_file', '05_worker.md'))
                    elif function_name == 'contact_moderator':
                        result = contact_moderator(args.get('message'), args.get('priority', 'NORMAL'))
                    elif function_name == 'send_message':
                        result = send_message(args.get('recipient_name'), args.get('message'))
                    elif function_name == 'read_file':
                        result = read_file(args.get('path'))
                    elif function_name == 'write_file':
                        result = write_file(args.get('path'), args.get('content'))
                    
                    print(f"Tool Result: {result}")
                        
                    self.messages.append({
                        'role': 'tool',
                        'content': result,
                    })
                    save_state() # Save after tool result
            else:
                final_answer = message['content']
                print(f"{self.name}: {final_answer}")
                break
        
        return final_answer

def main():
    global AGENTS
    print("=== Agent Orchestrator ===")
    
    # Try loading state first
    if load_state():
        print("Sitzung wiederhergestellt.")
        # print("\n[System] Starte Coding-Interfaces (Aider) für wiederhergestellte Agenten...")
        # for key, agent in AGENTS.items():
        #     launch_aider(agent.name)
    else:
        print("Initialisiere neue Session...")
        print("Initialisiere Sub-Agenten...")
        
        # Init Agents
        # Product Manager has contact_moderator, send_message, read_file, write_file
        prod_man = MistralAgent("Produktmanager", "02_Produktmanager", "02_Produktmanager.md", tools=[contact_moderator, send_message, read_file, write_file])
        
        # Architekt has init_worker, contact_moderator, send_message, read_file, write_file
        architekt = MistralAgent("Systemarchitekt", "03_Systemarchitekt", "03_Systemarchitekt.md", tools=[init_worker, contact_moderator, send_message, read_file, write_file])
        
        AGENTS["1"] = prod_man
        AGENTS["2"] = architekt
        save_state() # Initial save
        
        # Launch Aider for initial agents
        # print("\n[System] Starte Coding-Interfaces (Aider) für Agenten...")
        # launch_aider("Produktmanager")
        # launch_aider("Systemarchitekt")

    print("\nAlle Agenten bereit.")
    
    while True:
        print("\n=== MENÜ ===")
        # Dynamic Menu
        for key, agent in AGENTS.items():
            print(f"{key}: Chat mit {agent.name}")
        print("q: Beenden")
        
        choice = input("\nAuswahl: ")
        
        if choice.lower() == 'q':
            save_state()
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
