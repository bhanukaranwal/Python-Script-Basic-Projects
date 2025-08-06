import pandas as pd
import matplotlib.pyplot as plt
import speech_recognition as sr
import pyttsx3
import sys
import os

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        print("Speech could not play. Text output only.")

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say your command (e.g., 'sum column A'): ")
        audio = recognizer.listen(source)
    try:
        cmd = recognizer.recognize_google(audio)
        print("Heard:", cmd)
        return cmd.lower()
    except Exception as e:
        print("Sorry, could not recognize.", e)
        return ""

def process_command(df, cmd):
    result = None
    spoken = ""
    if "sum column" in cmd:
        col = cmd.split("sum column")[-1].strip().split(" ")[0].upper()
        try:
            val = df[col].sum()
            result = f"Sum of {col}: {val}"
            spoken = result
        except Exception:
            result = f"Column {col} not found."
            spoken = result
    elif "max column" in cmd or "maximum column" in cmd:
        col = cmd.split("column")[-1].strip().split(" ")[0].upper()
        try:
            val = df[col].max()
            result = f"Maximum of {col}: {val}"
            spoken = result
        except Exception:
            result = f"Column {col} not found."
            spoken = result
    elif "min column" in cmd:
        col = cmd.split("column")[-1].strip().split(" ")[0].upper()
        try:
            val = df[col].min()
            result = f"Minimum of {col}: {val}"
            spoken = result
        except Exception:
            result = f"Column {col} not found."
            spoken = result
    elif "mean column" in cmd or "average column" in cmd:
        col = cmd.split("column")[-1].strip().split(" ")[0].upper()
        try:
            val = df[col].mean()
            result = f"Mean of {col}: {val}"
            spoken = result
        except Exception:
            result = f"Column {col} not found."
            spoken = result
    elif "filter" in cmd:
        # filter out <col> <value>
        try:
            parts = cmd.split("filter out")[-1].strip().split(" ")
            col, val = parts[0].upper(), parts[1]
            n0 = len(df)
            df2 = df[df[col] != float(val)]
            result = f"Filtered {col} != {val}; {n0-len(df2)} rows removed."
            spoken = result
            df[:] = df2
        except Exception:
            result = "Could not parse filter command."
            spoken = result
    elif "plot" in cmd or "graph" in cmd:
        try:
            parts = cmd.split("plot")[-1].split("vs")
            if len(parts)==2:
                y, x = parts[0].strip().upper(), parts[1].strip().upper()
            else:
                y, x = parts[0].strip().upper(), None
            df.plot(x=x, y=y) if x else df[y].plot()
            plt.title(f"{y} vs {x}" if x else y)
            plt.savefig("voice_plot.png")
            plt.show()
            result = f"Plot saved as voice_plot.png"
            spoken = result
        except Exception:
            result = "Parse error for plot command."
            spoken = result
    elif "read head" in cmd or "top rows" in cmd:
        n = 5
        try:
            print(df.head(n))
            result = f"Displayed top {n} rows."
            spoken = result
        except Exception:
            result = "Could not display."
            spoken = result
    elif "exit" in cmd or "quit" in cmd or "stop" in cmd:
        print("Exiting.")
        sys.exit(0)
    else:
        result = "Unsupported or unclear command."
        spoken = result
    if spoken:
        speak(spoken)
    return result

def main():
    print("=== Voice-Controlled Spreadsheet Automation Bot ===")
    csvfile = input("CSV/Excel filename (will force upper col names): ").strip()
    if not os.path.exists(csvfile):
        print("File not found!")
        sys.exit(1)
    if csvfile.endswith(".csv"):
        df = pd.read_csv(csvfile)
    else:
        df = pd.read_excel(csvfile)
    df.columns = [c.upper() for c in df.columns]
    print(f"Columns: {list(df.columns)}")

    while True:
        cmd = listen_command()
        if not cmd:
            continue
        res = process_command(df, cmd)
        print(res)

if __name__ == "__main__":
    print("Dependencies: pandas, matplotlib, speech_recognition, pyttsx3")
    main()
