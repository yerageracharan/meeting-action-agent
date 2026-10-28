![Meeting Action Agent hero](assets/hero.svg)

# Meeting Action Agent

**Day 02 of the 200 AI Agents in 200 Days challenge**

Turn messy meeting notes into a practical action plan: decisions, tasks, owners, deadlines, open questions, and blockers.

**The most important rule:** if your notes do not name an owner or deadline, the agent should leave it unknown instead of making one up. It also checks that every task has a supporting quote copied from your notes. These safeguards help, but they do not replace a human reviewing the final report.

**New here? Start with the [Beginner Quick Start](#beginner-quick-start-windows).** You do not need to know what an API is before you begin.

[Download the full project ZIP](https://github.com/yerageracharan/meeting-action-agent/archive/refs/heads/main.zip) · [Download the visual PDF setup guide](docs/Local-AI-and-API-Setup-Guide.pdf) · [Open the detailed setup guide](docs/Local-AI-and-API-Setup-Guide.md)

---

## 1. What does this agent actually do?

Imagine your team finishes a meeting. People talked quickly, a few decisions were made, some jobs were assigned, and two important questions were left unanswered. Your notes might look like this:

> Priya will send the updated landing-page copy to Marcus by Thursday.  
> Marcus agreed to review the copy after he receives it.  
> We discussed adding a customer FAQ, but nobody was assigned to write it.  
> Alex will send the event-name list by Friday.  
> The team decided to keep the launch date unchanged for now.  
> Are we including the mobile screenshots in the launch email?  
> The legal review may take longer than planned.

You can understand those notes, but you still need to turn them into a list of things that need to happen. Meeting Action Agent helps do that.

It can produce:

- **A short summary:** what the meeting was about.
- **Decisions:** what the notes explicitly say the team agreed to.
- **Action items:** work that someone needs to do.
- **Owners:** who is responsible, if the notes name someone.
- **Deadlines:** when the work is due, if the notes say so.
- **Open questions:** things that still need an answer.
- **Risks and blockers:** issues that may delay the work.
- **Evidence quotes:** exact snippets from the notes that support each action.
- **Two report formats:** Markdown, which is easy for people to read, and JSON, which other software can process.

![Meeting notes becoming a clear action plan](assets/workflow.svg)

### What this project does not do

It does not join meetings, record audio, transcribe recordings, send emails, update your calendar, or create tasks inside apps such as Jira or Trello. You provide written notes, and it creates a report for you to review.

Think of it as a careful assistant who prepares the first draft of your follow-up list—not someone who is allowed to make business decisions for you.

## 2. Before you start: choose the easiest route

You need two things:

1. **Meeting Action Agent:** the Python project in this repository.
2. **A language model:** the AI that reads your notes and drafts the action plan.

You can run the model on your own computer with LM Studio or Ollama, or use a hosted AI service through an API.

![Local AI versus hosted API](assets/model-routes.svg)

| Choice | Cost and keys | What happens to your notes? | Best for |
|---|---|---|---|
| **Local model with LM Studio** | No paid provider key is normally needed | The model runs on your computer | People who want local processing |
| **Local model with Ollama** | No paid provider key is normally needed | The model runs on your computer | People comfortable with a small command-line setup |
| **Hosted API** | Requires a provider key; usage may cost money | Your request is sent to that provider | People whose computers cannot comfortably run a model |

**My beginner recommendation:** use LM Studio if you prefer a desktop app with buttons and menus. Use a hosted API if you do not want to download a model and your computer has limited memory. The hosted route may cost money, so check pricing and set spending limits first.

A local model can still require a one-time download and enough computer memory. “Local” does not mean that every model will run quickly on every laptop.

---

# Beginner Quick Start (Windows)

This section assumes you are using Windows 10 or Windows 11. Go one step at a time. You do not need to run all the commands at once.

## Step 1 — Download the project

1. Open this repository in your browser: [Meeting Action Agent on GitHub](https://github.com/yerageracharan/meeting-action-agent).
2. Find the green **Code** button near the top of the file list.
3. Click **Code**, then choose **Download ZIP**.
4. Wait for the download to finish. It normally appears in your **Downloads** folder.
5. Open File Explorer and go to **Downloads**.
6. Right-click the downloaded ZIP file and choose **Extract All…**.
7. Click **Extract**.
8. Open the extracted folder. Inside it, you should see files such as `README.md`, `pyproject.toml`, `app.py`, and folders such as `meetagent`, `examples`, and `tests`.

**Important:** open the folder that contains `pyproject.toml`. Do not run the commands from the Downloads folder above it, and do not open only the `assets` or `docs` folder.

If you prefer to download directly, use the [Download ZIP link](https://github.com/yerageracharan/meeting-action-agent/archive/refs/heads/main.zip).

## Step 2 — Install Python

Python is the programming language this project uses.

1. Open [python.org/downloads](https://www.python.org/downloads/).
2. Download a recent Python 3.10 or newer version for Windows.
3. Open the installer.
4. If the installer shows the option **Add Python to PATH**, tick it before continuing.
5. Click **Install Now** and wait until the installer finishes.
6. Close any old PowerShell windows and open a new one so Windows can find the new Python installation.

To check that Python is installed:

1. Press the Windows key.
2. Type **PowerShell**.
3. Open **Windows PowerShell** or **Terminal**.
4. Type this command and press Enter:

```powershell
python --version
```

You should see a version number, for example `Python 3.12.x`. The exact version can differ.

If Windows says that Python is not recognised, try:

```powershell
py --version
```

If `py` works but `python` does not, use `py` in place of `python` in the remaining commands. If neither command works, reinstall Python and make sure the PATH option is enabled.

## Step 3 — Open PowerShell in the correct project folder

This is the window where you will enter the commands.

**The easiest method:**

1. Open the extracted project folder in File Explorer.
2. Click the address bar at the top of the window—the place that shows the folder path.
3. Type `powershell`.
4. Press Enter.

A PowerShell window should open at that folder.

Check that it is the correct folder by typing:

```powershell
dir
```

Press Enter. You should see `pyproject.toml`, `README.md`, `app.py`, and the `meetagent` folder in the list.

If you do not see `pyproject.toml`, you are probably in the wrong folder. Return to File Explorer and open the project folder that contains it.

## Step 4 — Create a separate Python environment

A **virtual environment** is simply a separate space for this project's Python packages. It helps keep this project from interfering with other Python projects on your computer.

Copy this command into PowerShell and press Enter:

```powershell
python -m venv .venv
```

Wait for it to finish. It may not print a success message—that is normal.

Now activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation works, the terminal prompt usually starts with `(.venv)`.

### If Windows blocks the activation command

You may see a message about scripts being disabled. This is a common PowerShell setting issue. In the same PowerShell window, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

If asked to confirm, follow the prompt. This change applies only to the current PowerShell process. Then retry:

```powershell
.\.venv\Scripts\Activate.ps1
```

You can also skip activation and call the environment's Python directly, but activating it is easier for beginners.

## Step 5 — Install the project packages

Packages are pieces of code the project uses. The first install needs an internet connection and may take a little time.

Copy and run:

```powershell
python -m pip install --upgrade pip
```

When that finishes, install the project, test tools, and optional browser interface:

```powershell
python -m pip install -e ".[test,ui]"
```

Wait until PowerShell returns to the prompt. Some messages may be informational warnings; look for a final error before assuming installation failed.

You do **not** need to install every AI package or a paid API to install this project. The model itself is started separately in the next step.

## Step 6 — Confirm the code is installed correctly

Run the automated tests:

```powershell
python -m pytest -q
```

The current project includes five small tests for things such as empty notes, evidence checks, missing deadlines, and report formatting. A successful result should end with a summary similar to:

```text
5 passed
```

The exact time and punctuation may vary. These tests use simulated model responses, so they check the project logic but do not prove that every real AI model will behave correctly.

If you see `No module named pytest`, make sure you ran the package installation command from Step 5 in the activated environment.

## Step 7 — Choose and start your AI model

**Do this before asking the agent to process notes.** The project code needs a model server to be running, unless you choose a hosted API.

### Route A — LM Studio (recommended for a button-based desktop setup)

![Five steps for setting up LM Studio](assets/lmstudio-flow.svg)

1. Visit [lmstudio.ai](https://lmstudio.ai/) and download the Windows version.
2. Install and open LM Studio.
3. Open its **Discover** or model-search area.
4. Search for a small *instruct* model. An instruct model is trained to follow requests and is a useful starting point for this kind of task.
5. Check the download size shown by LM Studio before downloading. If you are unsure how powerful your computer is, start with a smaller model.
6. Download the model and wait for the progress to finish.
7. Load the downloaded model in the Chat screen. Try a simple request to check that it responds.
8. Open the **Developer** tab and start the local server.
9. Keep LM Studio open while using the agent.

LM Studio commonly uses a local address such as `http://localhost:1234/v1`. Use the actual address shown in your installation.

Now return to the PowerShell window where you installed this project and set the connection. Replace the example model ID with the exact ID shown by your LM Studio server:

```powershell
$env:MEETAGENT_BASE_URL = "http://localhost:1234/v1"
$env:MEETAGENT_MODEL = "YOUR-EXACT-LOADED-MODEL-ID"
Remove-Item Env:MEETAGENT_API_KEY -ErrorAction SilentlyContinue
```

To find the model ID provided by the server, run:

```powershell
Invoke-RestMethod http://localhost:1234/v1/models | ConvertTo-Json -Depth 5
```

Look at the result and copy the exact model ID into the second command. Do not type the placeholder text literally.

**What does localhost mean?** It means “this same computer.” Your agent sends requests to the model server running on your machine.

Official instructions: [Download a model in LM Studio](https://lmstudio.ai/docs/app/basics/download-model) · [Start its local server](https://lmstudio.ai/docs/developer/core/server).

### Route B — Ollama (another local option)

1. Download Ollama from [ollama.com/download](https://ollama.com/download).
2. Install it and make sure Ollama is running.
3. Open PowerShell. Download a small starter model with:

```powershell
ollama pull qwen2.5:3b
```

The first download requires an internet connection and can take time. It also uses disk space.

4. Point this project at Ollama:

```powershell
$env:MEETAGENT_BASE_URL = "http://localhost:11434/v1"
$env:MEETAGENT_MODEL = "qwen2.5:3b"
Remove-Item Env:MEETAGENT_API_KEY -ErrorAction SilentlyContinue
```

Keep Ollama running while you use the agent. These environment settings apply to the current PowerShell session. If you open a new terminal later, you may need to enter them again.

Official documentation: [Ollama](https://docs.ollama.com/).

### Route C — Hosted API (no model download required)

A hosted API lets a company run the model on its servers. Your computer does not need to hold the model files, but you need internet access and usually an API key. Usage may cost money.

For example, if you use the OpenAI API:

1. Open [OpenAI API key settings](https://platform.openai.com/api-keys).
2. Sign in and create an API key if your account is eligible.
3. Check your API billing and usage settings before sending requests.
4. Set the following variables in PowerShell, using a model name supported by your provider:

```powershell
$env:MEETAGENT_BASE_URL = "https://api.openai.com/v1"
$env:MEETAGENT_MODEL = "YOUR-SUPPORTED-MODEL-ID"
$env:MEETAGENT_API_KEY = "YOUR-SECRET-API-KEY"
```

Replace both placeholders. Do not run the command with placeholder text and expect it to work.

**Keep API keys private.** Do not put the real key in this README, Python files, screenshots, GitHub, or a public chat. Hosted API usage is generally billed separately from a ChatGPT subscription. Check the provider's current pricing and terms directly.

### What if LM Studio asks for an API key?

Some local servers can have authentication switched on. If you deliberately enabled authentication, use the local server token shown by LM Studio in `MEETAGENT_API_KEY`. That is a token for your own local server—not the same thing as a paid hosted-provider key.

If you did not enable local-server authentication, you can usually leave the API key unset for local use.

More details: [LM Studio authentication guide](https://lmstudio.ai/docs/developer/core/authentication).

## Step 8 — Run the first example

Make sure the model server is running and you have completed the matching model setup above.

In the project PowerShell window, run:

```powershell
python -m meetagent.cli "examples/meeting_notes.txt" --out "output/action_plan.md"
```

The first request might take longer as the model wakes up or loads. Wait for the command to finish.

A successful run should print where it saved the results, including paths similar to:

```text
Action plan saved to: output/action_plan.md
JSON data saved to: output/action_plan.json
```

Now open the project folder in File Explorer and go into the `output` folder. You should see:

- `action_plan.md` — the report you can open in a text editor or Markdown viewer.
- `action_plan.json` — the same structured information saved in a format software can read.

The program creates the output folder when needed. Generated reports are ignored by Git so private meeting information is not accidentally committed to the public repository.

## Step 9 — Try your own meeting notes

You do not need to edit Python code to use your own notes.

1. Open Notepad.
2. Type or paste your meeting notes. For example:

```text
Team planning meeting

Maya will send the draft proposal to Rohan by Friday.
Rohan agreed to review it next week.
We discussed a website redesign, but nobody owns that task yet.
The launch date is still undecided.
The finance team needs to confirm the available budget.
```

3. In Notepad, choose **File → Save As**.
4. Browse to your project's `examples` folder.
5. Name the file `my_meeting.txt`.
6. For **Save as type**, choose **All files** if that option appears. Make sure the final file name ends in `.txt`, not `.txt.txt`.
7. Save the file.

Back in PowerShell, run:

```powershell
python -m meetagent.cli "examples/my_meeting.txt" --out "output/my_action_plan.md"
```

Open `output/my_action_plan.md` to review the plan. Compare it against your original notes. If a name, date, decision, or task is wrong, correct the report manually before sharing it.

## Step 10 — Use the browser interface instead of the command line (optional)

If you prefer a simple page with a text box and a button, the project has an optional web interface.

First, make sure you installed the `ui` extra in Step 5. Start the app from the project folder:

```powershell
streamlit run app.py
```

PowerShell should print a local address, often something like `http://localhost:8501`. Hold **Ctrl** and click the address, or copy it into your browser.

1. Paste your meeting notes into the large text box.
2. Click **Create action plan**.
3. Wait for the result. A local model may take several seconds or longer.
4. Read through the summary and action items.
5. Use the download button to save the Markdown report.

Keep the PowerShell window and model server open while using the app. To stop the Streamlit app, go back to its PowerShell window and press **Ctrl+C**.

If you see an error in the browser, read the red error message and the corresponding terminal output. The troubleshooting section below explains the most common problems.

---

## How the agent works (plain English)

![How notes become an action plan](assets/workflow.svg)

1. **Read the notes.** The input is a plain-text file or text pasted into the browser page.
2. **Ask the model to organise them.** The prompt asks for a fixed JSON format instead of a free-form essay.
3. **Check the response structure.** The program confirms that the response contains the expected fields.
4. **Check evidence.** Every proposed action needs a quote that appears exactly in the original notes. If the quote is missing, the program rejects the output.
5. **Flag missing details.** If an owner or deadline is unknown, the task is marked for clarification instead of inventing information.
6. **Write the reports.** The final Markdown is readable by people. JSON is useful if another program needs the data.

![The checks that help catch unsupported actions](assets/guardrails.svg)

The checks are not a guarantee of truth. A model might still misunderstand a sentence or miss an action entirely. Always review the result—especially when it contains deadlines, commitments, budgets, legal details, or sensitive information.

## Understand the model settings

You may see these terms in setup instructions:

- **Model:** the AI system you want to use, such as a model loaded in LM Studio or Ollama.
- **Model ID:** the exact label the server uses to identify the loaded model. Copy it from the server instead of guessing.
- **Base URL:** the address of the server. For local models, it usually begins with `http://localhost:`.
- **API key:** a secret token that proves you are allowed to use a hosted provider. Keep it private.
- **Local model:** the model runs on your computer; it still needs enough memory and disk space.
- **Hosted model:** the model runs on another company's servers; requests need the internet and may be billed.
- **Quantization (Q4/Q5/Q8):** a method of shrinking a model to use less memory. Smaller versions may run more easily, but quality can vary.
- **RAM:** your computer's working memory.
- **VRAM:** memory on a dedicated graphics card.
- **Endpoint:** the URL where a program sends requests to the model.

## Pick a model that fits your computer

![A rough local model hardware guide](assets/hardware-picker.svg)

The categories in the visual are only starting points, not guarantees. Performance depends on the exact model, quantization, context length, RAM, GPU memory and other running apps. Check the size and memory estimate shown in LM Studio before starting a large download. Start small; upgrade only if it runs comfortably.

You can open the separate [Local AI and API Setup PDF](docs/Local-AI-and-API-Setup-Guide.pdf) for visual guidance or read the [Markdown setup guide](docs/Local-AI-and-API-Setup-Guide.md).

## Run the tests again whenever you change the project

From the project folder, with the correct environment active:

```powershell
python -m pytest -q
```

The current tests use mocked responses. They check specific logic paths; they do not test the performance of every real model or guarantee that the agent's output is factually perfect.

## Troubleshooting: common problems and fixes

### “Python is not recognised” or “python was not found”

- Install Python from [python.org](https://www.python.org/downloads/).
- If the installer offers **Add Python to PATH**, select it.
- Close and reopen PowerShell after installation.
- Try `py --version`; if it works, use `py` instead of `python`.

### “No module named meetagent”

- Return to the folder that contains `pyproject.toml`.
- Activate the `.venv` environment.
- Run `python -m pip install -e ".[test,ui]"` again.
- Make sure you are using the same PowerShell window/environment for installation and running.

### “Could not reach the model server”

- Open LM Studio or make sure Ollama is running.
- In LM Studio, confirm the local server is started in Developer.
- Check that `MEETAGENT_BASE_URL` matches the address displayed by the model tool.
- Keep the `/v1` suffix in the base URL. The project adds `/chat/completions` to it.
- Remember that environment variables set with PowerShell's `$env:` syntax apply only to that PowerShell session. If you opened a new window, run the setup commands again.

### “Model not found” or “unknown model”

- In LM Studio, ask the server to list its models using the command in Step 7.
- Copy the model ID exactly as shown, including punctuation and capitalization.
- For Ollama, check the models you have downloaded with `ollama list`.
- Make sure the model is actually downloaded and loaded or available to the server.

### “The model returned invalid JSON”

The program asks the model for structured data, but some models do not follow those instructions reliably.

- Try a smaller, instruction-following model known to produce structured output.
- Shorten very long meeting notes.
- Try again once the model is fully loaded.
- If the problem continues, use a compatible hosted model or report the issue with the error message. Do not include secret API keys in the report.

### “An action item was rejected because the evidence quote is missing”

That is intentional. The project checks whether the model's evidence quote appears exactly in the original notes. A paraphrase may fail the exact-match check. Review the note and the rejected output; do not disable the check simply to make the warning go away.

### “There is no owner or deadline”

That is expected if the notes do not specify one. The agent should not guess. Assign an owner or deadline yourself after confirming it with the team.

### “The computer is slow or runs out of memory”

- Download a smaller model or a more compressed quantized version.
- Close other large apps and unload other models.
- Try a shorter input.
- Check the memory estimate before loading the model.
- If local models are not practical on your computer, consider a hosted API after checking its pricing and privacy terms.

### “The API key is invalid” or “I get a billing error”

- Check that you copied the provider's key correctly.
- Check that the selected model is available to your account.
- Confirm the base URL and model ID are correct.
- Check the provider's account, billing and usage limits.
- Do not put your key in GitHub or send it to anyone helping troubleshoot.

### “Streamlit is not recognised”

Install the optional interface and run Streamlit through Python:

```powershell
python -m pip install -e ".[ui]"
python -m streamlit run app.py
```

## Privacy and safety

Meeting notes can contain names, budgets, customer details or confidential plans.

- With a hosted API, your notes are sent to the provider. Only send content you are permitted to share.
- With a local model, processing can stay on your computer, but make sure you are connecting to your own local server and understand any tools/extensions you have enabled.
- Never commit secret keys, passwords, or private meeting notes to a public repository.
- Treat the generated plan as a draft. Verify decisions, names, owners and deadlines before sharing or acting on it.
- Do not rely on this tool alone for legal, financial, medical or other high-stakes decisions.

## Project layout

```text
app.py                             Optional browser interface
meetagent/
  __init__.py                      Package version
  agent.py                         Prompt, JSON validation, evidence checks
  provider.py                      Local/hosted API connection
  cli.py                           Command-line interface
  render.py                        Markdown and JSON report writer
examples/
  meeting_notes.txt                Example input
tests/
  test_agent.py                    Automated tests
assets/
  hero.svg                         Main project illustration
  workflow.svg                     Notes-to-action workflow
  model-routes.svg                 Local versus hosted choices
  lmstudio-flow.svg                LM Studio setup steps
  guardrails.svg                   Evidence and safety checks
  hardware-picker.svg              Hardware selection guide
docs/
  Local-AI-and-API-Setup-Guide.md  Full written setup guide
  Local-AI-and-API-Setup-Guide.pdf Visual setup guide
output/                            Generated reports (not committed)
pyproject.toml                     Python package and dependencies
.env.example                       Example settings only; not loaded automatically
LICENSE                            MIT license
```

## Future improvements

Possible next steps include support for Word documents and transcripts, better handling of unclear speakers, exporting to calendar/task systems with explicit user approval, broader tests on real anonymised notes, and comparisons across local and hosted models. These features are ideas—not features this version already provides.

## License

MIT. See [LICENSE](LICENSE).

---

**Day 02 / 200.** One agent at a time. Build it, test it, document it, improve it.
