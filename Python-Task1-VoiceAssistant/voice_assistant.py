"""
=============================================================================
Project Name   : Python Voice Assistant
Task           : Task 1 — Voice Assistant
Track          : Python Programming
Internship     : Oasis Infobyte SIP
Author         : raj changani
Description    : A clean, modular, and beginner-friendly Python voice assistant.
                 Features voice input (SpeechRecognition), text-to-speech (pyttsx3),
                 time and date retrieval, web searching via Google, and robust
                 error handling.
=============================================================================
"""

import sys
import datetime
import webbrowser
import urllib.parse
import speech_recognition as sr
import pyttsx3

# =============================================================================
# GLOBAL INITIALIZATION & CONFIGURATION
# =============================================================================

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Speech synthesis configuration
SPEECH_RATE = 175    # 175 provides natural, clear speaking pace
SPEECH_VOLUME = 1.0  # Full volume (0.0 to 1.0)

# Flag to track whether microphone hardware is functional
MIC_AVAILABLE = True


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def speak(text: str) -> None:
    """
    Speaks the provided text aloud using pyttsx3 and displays it in the terminal.
    Re-initializes the TTS engine per utterance to ensure continuous speech audio
    on Windows (SAPI5) and prevent subsequent commands from falling silent.
    
    Parameters:
        text (str): The response string to display and speak aloud.
    """
    if not text:
        return

    # Always display the response in the terminal / chat interface
    print(f"\n[Assistant]: {text}")

    # Speak aloud via text-to-speech
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", SPEECH_RATE)
        engine.setProperty("volume", SPEECH_VOLUME)
        engine.say(text)
        engine.runAndWait()
        del engine
    except Exception as err:
        print(f"[Audio Output Error]: Could not play speech audio ({err})")


def listen(text_mode: bool = False) -> str | None:
    """
    Captures voice input from the user's microphone and converts it to text
    using Google Speech Recognition. If microphone access is unavailable or
    text_mode is enabled, gracefully falls back to console keyboard input.
    
    Parameters:
        text_mode (bool): If True, accepts text input from console directly.
        
    Returns:
        str: The recognized command in lowercase, or None if recognition fails.
    """
    global MIC_AVAILABLE

    # Direct text-input mode (useful for testing or systems without a mic)
    if text_mode or not MIC_AVAILABLE:
        try:
            command = input("\n[User (typed)]: ").strip()
            return command.lower() if command else None
        except (EOFError, KeyboardInterrupt):
            return "exit"

    # Voice-input mode via microphone
    try:
        with sr.Microphone() as source:
            print("\n[*] Listening... (speak clearly into your microphone)")
            
            # Calibrate for ambient room noise to enhance accuracy
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            
            # Capture speech with timeout to prevent hanging
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            
            print("[*] Processing speech...")
            # Convert spoken audio into text via Google Speech Recognition
            command = recognizer.recognize_google(audio)
            
            # Display recognized speech in terminal
            print(f"[User]: {command}")
            return command.strip().lower()

    except sr.WaitTimeoutError:
        # User did not speak within the timeout window
        print("[-] Listening timed out. No speech detected.")
        return None

    except sr.UnknownValueError:
        # Audio was detected but could not be understood
        error_msg = "Sorry, I could not understand you. Please repeat."
        speak(error_msg)
        return None

    except sr.RequestError as req_err:
        # Google Speech API unreachable / network connectivity error
        error_msg = f"Network error: Unable to reach speech recognition service ({req_err})."
        speak(error_msg)
        return None

    except (OSError, AttributeError) as mic_err:
        # PyAudio not installed or microphone hardware unavailable
        MIC_AVAILABLE = False
        print(f"\n[!] Microphone Warning: {mic_err}")
        print("[!] Note: PyAudio or microphone hardware is not accessible on this system.")
        print("[*] Automatically switching to text input mode for remaining session...")
        speak("Microphone is currently unavailable. You can type your commands below.")
        try:
            command = input("\n[User (typed)]: ").strip()
            return command.lower() if command else None
        except (EOFError, KeyboardInterrupt):
            return "exit"

    except Exception as general_err:
        # Catch-all to ensure the assistant never crashes unexpectedly
        print(f"\n[!] Unexpected Error during listening: {general_err}")
        return None


def handle_command(command: str | None) -> bool:
    """
    Processes and executes user commands based on keyword recognition.
    
    Parameters:
        command (str | None): The user's recognized spoken or typed command.
        
    Returns:
        bool: True to continue listening, False to safely terminate the assistant.
    """
    # Graceful handling for empty or None commands
    if not command or not command.strip():
        return True

    command = command.strip().lower()

    # -------------------------------------------------------------------------
    # 1. Exit Commands (Safe Termination)
    # -------------------------------------------------------------------------
    exit_triggers = ["exit", "quit", "stop", "goodbye", "bye"]
    if any(command == trigger or command.startswith(f"{trigger} ") for trigger in exit_triggers):
        farewell = "Goodbye! Have a great day!"
        speak(farewell)
        return False

    # -------------------------------------------------------------------------
    # 2. Greeting Commands
    # -------------------------------------------------------------------------
    greeting_triggers = ["hello", "hi", "hey", "greetings"]
    if any(command == trigger or command.startswith(f"{trigger} ") or f" {trigger} " in f" {command} " for trigger in greeting_triggers):
        greeting_response = "Hello! How can I help you today?"
        speak(greeting_response)
        return True

    # -------------------------------------------------------------------------
    # 3. Current Time Command
    # -------------------------------------------------------------------------
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        time_response = f"The current time is {current_time}."
        speak(time_response)
        return True

    # -------------------------------------------------------------------------
    # 4. Current Date Command
    # -------------------------------------------------------------------------
    if "date" in command or "today" in command:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        date_response = f"Today's date is {current_date}."
        speak(date_response)
        return True

    # -------------------------------------------------------------------------
    # 5. Web Search Command
    # -------------------------------------------------------------------------
    if "search" in command or command.startswith("google"):
        # Extract query topic by stripping recognized prefixes
        query = command
        for prefix in ["search for", "search", "google for", "google"]:
            if query.startswith(prefix):
                query = query[len(prefix):].strip()
                break

        query = query.strip()

        if not query:
            speak("What would you like me to search for?")
            return True

        # Speak confirmation and open search in default browser
        speak(f"Searching for {query}.")
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(search_url)
        return True

    # -------------------------------------------------------------------------
    # 6. Unrecognized Command Fallback
    # -------------------------------------------------------------------------
    speak("Sorry, I could not understand you. Please repeat.")
    return True


def display_banner() -> None:
    """Prints a clean ASCII welcome banner to the terminal."""
    banner = """
=============================================================
                PYTHON VOICE ASSISTANT
            Oasis Infobyte SIP - Task 1
=============================================================
Supported Commands:
  - Greeting    : "Hello", "Hi", "Hey"
  - Current Time: "What is the time?", "Tell me the time"
  - Current Date: "What is today's date?", "Today's date"
  - Web Search  : "Search Python programming", "Search AI"
  - Exit        : "Exit", "Quit", "Stop", "Goodbye"
=============================================================
"""
    print(banner)


# =============================================================================
# MAIN FUNCTION & ENTRY POINT
# =============================================================================

def main() -> None:
    """
    Main entry point for the Voice Assistant.
    Supports optional '--text' flag for testing without microphone hardware.
    """
    text_mode = "--text" in sys.argv

    display_banner()

    # Initial spoken greeting on startup
    startup_message = "Hello! I am your Python Voice Assistant. How can I help you?"
    speak(startup_message)

    if text_mode:
        print("\n[*] Running in Text-Input Mode (--text flag detected).")

    # Continuous listening loop
    running = True
    try:
        while running:
            # Capture user command
            user_command = listen(text_mode=text_mode)
            
            # Process command; returns False upon receiving exit commands
            running = handle_command(user_command)

    except KeyboardInterrupt:
        # Graceful handling for Ctrl+C
        print("\n\n[*] Voice Assistant stopped by user. Exiting cleanly...")
        speak("Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
