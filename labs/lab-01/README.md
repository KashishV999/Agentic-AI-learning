# Lab 1

## Code Flow

### 1. Check API Key
- Verify if `OPENROUTER_API_KEY` is set in the environment variables.
- If not found, print an error message and exit the program.

### 2. Get Staged Git Diff
- Use `subprocess` (`git diff --staged`) to retrieve the staged Git diff.
- Store the diff in a variable for later processing.

### 3. Generate Commit Message
- Define a `chatCompletion()` function to generate a semantic commit message.
- Send the staged diff to the OpenRouter API using the OpenAI SDK.

### 4. Handle `--creative` Flag
- Check if the `--creative` flag is provided.
- If enabled:
  - Use a higher temperature.
  - Apply a more imaginative system prompt.
- Otherwise:
  - Use a lower temperature.
  - Apply a more straightforward system prompt.

### 5. Print Commit Message
- In the `main()` function, call `chatCompletion()`.
- Print the generated commit message to the console.


## Usage

1. Stage your changes using `git add <file>`.
2. Run the script:
   ```bash
   python git_cm.py
   ```
3. For a more creative commit message, use:
   ```bash
   python git_cm.py --creative
   ```  