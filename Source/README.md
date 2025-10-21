# How to Run

## Prerequisites

- Python 3.6 or higher
- Download the `words` folder from [Google Drive](https://drive.google.com/drive/folders/1HxLSlxAeCmn4LgLzwkabLom3lTIEAET5?usp=drive_link)

## Project Structure

```
Source/
│
├── main.py           # Main program file
└── words/            # Word lists folder
    ├── word_lengths.txt
    ├── wordle-4.txt
    ├── wordle-5.txt
    └── ...
```

## Steps

1. Download and extract the `words` folder from the link above

2. Place the `words` folder in the project directory (same location as `main.py`)

3. Open Command Prompt (CMD)

4. Navigate to the project directory:

```bash
cd path\to\your\project\folder\24127003\Source
```

5. Run the program:

```bash
python main.py
```

or

```bash
python3 main.py
```

## Common Errors and Solutions

### Error: 'python' is not recognized as an internal or external command

**Cause:** Python is not installed or not added to PATH

**Solution:**

- Download and install Python from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"
- Or manually add Python to system PATH

### Error: "Không tìm thấy file 'words/wordle-X.txt'"

**Cause:** Word list files are missing

**Solution:**

- Ensure the `words/` folder exists in the project directory
- Make sure word list files (wordle-4.txt, wordle-5.txt, etc.) are present
- Check that `word_lengths.txt` file exists in the `words/` folder

### Error: ModuleNotFoundError: No module named 'tkinter'

**Cause:** Tkinter is not installed

**Solution:**

- **Windows:** Reinstall Python with "tcl/tk and IDLE" option checked
- **Linux:** Run `sudo apt-get install python3-tk`
- **macOS:** Run `brew install python-tk`

### Error: The system cannot find the path specified

**Cause:** Wrong directory path

**Solution:**

- Verify the correct path to your project folder
- Use `dir` command to check current directory
- Make sure to use quotes around path with spaces

### Error: Permission denied

**Cause:** Insufficient permissions to run the file

**Solution:**

- Run CMD as Administrator
- Check file permissions in Windows Explorer
