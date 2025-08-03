def emoji_chooser():
    moods = {
        "happy": "😊",
        "sad": "😢",
        "excited": "🤩",
        "angry": "😠"
    }
    print("How are you feeling? Pick one: happy, sad, excited, angry")
    mood = input("Your mood: ").lower()
    print("Here’s your emoji:", moods.get(mood, "🤔 Not sure how to show that!"))

if __name__ == "__main__":
    emoji_chooser()
