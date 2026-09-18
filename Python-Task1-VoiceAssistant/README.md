# Python Voice Assistant

An interactive, clean, and modular desktop Voice Assistant built in Python for the **Oasis Infobyte SIP (Python Programming Track) — Task 1**.

The assistant captures voice commands from the user's microphone, processes the request using speech recognition, performs designated actions (greetings, current time, current date, web searching), and responds with natural voice output via text-to-speech synthesis while displaying all activity in the terminal.

---

## Overview

The **Python Voice Assistant** acts as a virtual conversational desktop helper designed with a beginner-friendly yet robust architecture. It provides an intuitive hands-free interface for everyday tasks like checking the time and date or launching Google web searches.

Key highlights:

- **Speech Recognition**: Utilizes Google Speech Recognition via the `SpeechRecognition` library.
- **Natural Voice Synthesis**: Uses `pyttsx3` for offline, low-latency text-to-speech feedback.
- **Robust Exception Handling**: Prevents abrupt crashes when speech is unclear, network drops occur, or audio devices are disconnected.
- **Modular Design**: Separates audio capture, speech synthesis, and command processing into clean, reusable functions.

---

## Beginner Tier Requirements Mapping

The table below outlines how each mandatory requirement from the Oasis Infobyte SIP specification is mapped to its implementation in the codebase:

| Requirement                    | Implementation in `voice_assistant.py`    | Description                                                                                                                                                                                                                                                   |
| :----------------------------- | :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Voice Input**             | `listen()`                                | Captures microphone audio using `sr.Microphone()`, adjusts for ambient noise (`adjust_for_ambient_noise`), converts speech to text via Google Speech Recognition, and displays the recognized command in the terminal (`[User]: <command>`).                  |
| **2. Greeting**                | `handle_command()`                        | Detects greetings such as `"hello"`, `"hi"`, or `"hey"`, and responds with a friendly spoken and printed greeting (`"Hello! How can I help you today?"`).                                                                                                     |
| **3. Current Time**            | `handle_command()`                        | Retrieves the system's current time using `datetime.datetime.now()`, formats it in a 12-hour AM/PM format (e.g., `04:30 PM`), speaks it aloud, and prints it to the console.                                                                                  |
| **4. Current Date**            | `handle_command()`                        | Retrieves the current date using `datetime.datetime.now()`, formats it with weekday, month, day, and year (e.g., `Friday, September 18, 2026`), speaks it aloud, and prints it to the console.                                                                |
| **5. Web Search**              | `handle_command()`                        | Detects search requests (e.g., `"Search Python programming"`), extracts the query string, opens the query in the default browser on Google via `webbrowser.open()`, and speaks a voice confirmation.                                                          |
| **6. Graceful Error Handling** | `listen()`, `speak()`, `handle_command()` | Gracefully catches `sr.UnknownValueError` ("Sorry, I could not understand you. Please repeat."), `sr.RequestError` (network issues), `sr.WaitTimeoutError`, audio hardware errors (`OSError`/`AttributeError`), and empty/whitespace inputs without crashing. |

### Additional Quality Features

- **Clean Exit Commands**: Responds to `"exit"`, `"quit"`, `"stop"`, or `"goodbye"` with a farewell message and safely terminates the program.
- **Continuous Listening Loop**: Continuously listens for commands in `main()` until an exit command or `Ctrl+C` is received.
- **Startup Announcement**: Welcomes the user with a terminal banner and a spoken greeting on launch.
- **Modular Code Architecture**: Code is split into focused functions: `speak()`, `listen()`, `handle_command()`, `display_banner()`, and `main()`.

---

## Technologies Used

- **Python 3.x**: Core programming language.
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)**: Captures and processes microphone audio.
- **[pyttsx3](https://pypi.org/project/pyttsx3/)**: Offline text-to-speech synthesis.
- **[PyAudio](https://pypi.org/project/PyAudio/)**: PortAudio Python bindings for microphone stream access.
- **datetime** _(Python Standard Library)_: Retrieves system date and time.
- **webbrowser** _(Python Standard Library)_: Controls system web browser for web queries.
- **urllib.parse** _(Python Standard Library)_: Encodes URL query parameters.

---

## Project Structure

```
Python-Task1-VoiceAssistant/
│
├── voice_assistant.py     # Main application source code
├── README.md              # Project documentation and submission guide
├── requirements.txt       # Third-party Python dependencies
└── screenshots/           # Directory reserved for submission screenshots
    └── .gitkeep           # Ensures the directory is tracked in Git
```

---

## Installation

### 1. Check Python Version

Ensure Python 3.8 or higher is installed and accessible from your terminal:

```bash
python --version
```

### 2. Navigate to the Project Directory

```bash
cd Python-Task1-VoiceAssistant
```

### 3. Install Required Dependencies

Install third-party packages from `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

> **Windows Note for PyAudio**:
> On Windows, `pip install PyAudio` usually installs pre-compiled binary wheels. If you encounter a compiler error on your Python version, you can install PyAudio using `pipwin`:
>
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```
>
> Alternatively, if using Anaconda/Miniconda:
>
> ```bash
> conda install -c conda-forge pyaudio
> ```

---

## How to Run

Run the assistant from your terminal or command prompt:

```bash
python voice_assistant.py
```

1. Upon startup, the assistant displays a banner and speaks:
   > _"Hello! I am your Python Voice Assistant. How can I help you?"_
2. When the terminal prompts `[*] Listening...`, speak clearly into your microphone.
3. The recognized speech is printed with `[User]: <command>` and the response is spoken aloud.

_(Optional Testing Mode)_: To test the assistant using keyboard input without a microphone, run:

```bash
python voice_assistant.py --text
```

---

## Supported Commands

| Category         | Example Spoken Commands                                    | Action Performed                                        |
| :--------------- | :--------------------------------------------------------- | :------------------------------------------------------ |
| **Greeting**     | `"Hello"`, `"Hi"`, `"Hey"`                                 | Speaks and displays a friendly greeting.                |
| **Current Time** | `"What is the time?"`, `"Tell me the time"`                | Speaks and displays the current system time.            |
| **Current Date** | `"What is today's date?"`, `"Today's date"`                | Speaks and displays the current system date.            |
| **Web Search**   | `"Search Python programming"`, `"Search machine learning"` | Opens Google search in the default web browser.         |
| **Exit**         | `"Exit"`, `"Quit"`, `"Stop"`, `"Goodbye"`                  | Speaks farewell and terminates the application cleanly. |

---

## Error Handling

The application is built defensively to ensure continuous operation:

1. **Unrecognized Speech (`sr.UnknownValueError`)**:
   - If ambient noise or unclear speech prevents parsing, the assistant responds with:
     `"Sorry, I could not understand you. Please repeat."`
   - The loop continues to listen for subsequent commands.

2. **Service / Network Issues (`sr.RequestError`)**:
   - If the speech recognition API cannot be contacted, a network error message is spoken and displayed without terminating the program.

3. **Microphone Access Issues (`OSError` / Missing PyAudio)**:
   - If a recording device is missing or unconfigured, an informative error is shown in the console along with a graceful prompt, avoiding an unhandled crash.

4. **Empty Commands**:
   - Blank or silent inputs are ignored, allowing the assistant to continue listening.

---

## Screenshots

> _Note: Execution screenshots should be captured during testing and saved into the `screenshots/` directory prior to final submission. The `.gitkeep` file ensures the folder remains tracked in Git._

Suggested screenshots to capture:

- `screenshots/startup_and_greeting.png` — Assistant launch and greeting response.
- `screenshots/time_and_date.png` — Time and date query responses.
- `screenshots/web_search.png` — Web search command and browser launch.
- `screenshots/exit_command.png` — Safe exit upon termination command.

---

## Future Improvements

Potential enhancements for future iterations:

- **Natural Language Understanding (NLU)**: Integrate semantic intent detection (e.g., spaCy or an LLM API).
- **Weather API**: Fetch real-time weather forecasts via OpenWeatherMap.
- **Email & Reminders**: Voice-triggered reminders and email dispatching.
- **Offline Speech Recognition**: Add local offline engines like Vosk or Whisper.
- **Custom Wake Word**: Continuous background listening with a wake phrase (e.g., `"Hey Assistant"`).

---

## Author

- **Name**: raj changani
- **Track**: Python Programming
- **Task**: Task 1 — Voice Assistant
- **Internship**: Oasis Infobyte SIP
