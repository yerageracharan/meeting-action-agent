# Install and use Codebase Onboarding Agent

This is a portable Agent Skill folder. Products expose skills in different ways; plans, account settings, regions and workspace administrators may affect availability. The fallback that works in a normal chat is to paste SKILL.md into the conversation and provide the repository URL or source files.

## Claude

Claude supports skills in eligible Claude experiences when the required skills/code-execution capabilities are enabled. Use the current official docs because import UI can differ by surface and account:

- https://support.claude.com/en/articles/12512176-what-are-skills
- https://support.claude.com/en/articles/12512176-what-are-skills

If your Claude interface offers skill import, package this folder as a ZIP with SKILL.md at the skill folder root and upload it. If not, use the manual fallback below.

## ChatGPT and Codex

OpenAI Agent Skills availability depends on product surface and account/workspace eligibility. Current documentation describes standalone skills in the ChatGPT desktop app, Codex CLI and IDE extension; skills in supported plugins may have broader ChatGPT surface availability.

- https://learn.chatgpt.com/docs/build-skills
- https://help.openai.com/en/articles/20001066-skills-in-chatgpt

Where your client provides a skill installation path, install this folder as a skill. For Codex-style repository skills, check the current docs for the expected directory location. If your account does not expose native skill installation, paste SKILL.md into a conversation and attach the source ZIP.

## Gemini

Gemini has multiple product surfaces. Agent Skills are documented for Gemini CLI. The Gemini Apps custom Skills feature is currently documented for Gemini Spark and may require an eligible personal account, subscription and region.

- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- https://support.google.com/gemini/answer/17094296?hl=en

If Gemini Apps exposes a Skills page to your account, use its Upload option and select SKILL.md or a ZIP containing SKILL.md in the main folder. Do not assume the feature is enabled for every account.

## Manual fallback for any assistant

1. Open SKILL.md.
2. Copy its complete contents into the assistant's instructions, or upload the Markdown file if the chat accepts it.
3. Provide a public GitHub repository URL or upload the source ZIP.
4. Ask for a beginner-friendly codebase onboarding report.
5. If the assistant cannot access the URL, do not let it guess: upload the source or paste the file tree and important files.

This is not a persistent installed skill. You may need to provide the instructions again in a new chat.

## Limitations

The skill contains instructions, not a GitHub connector. It cannot independently access a private repository, browse the web, clone source, run a build or execute tests. Those actions work only if the assistant has the relevant connected tools and permissions. Do not provide access tokens or secrets in chat.
