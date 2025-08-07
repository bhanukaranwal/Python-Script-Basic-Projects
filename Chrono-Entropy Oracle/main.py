import random
import datetime
import time

COHERENT_ANSWERS = [
    "The path is clear and the stars align.",
    "Trust in the cycles; balance will be restored.",
    "Seek the hidden key within the shadows.",
    "An ancient force guides your journey forward.",
    "The river flows, carrying change with its current.",
]

SURREAL_FRAGMENTS = [
    "Th3 p@th 1s cl**r...",
    "Tru$t in cyc1es; b@l@nce w!ll b3 r3st@red.",
    "S33k h!dd3n k3y w!th!n sh@dows...",
    "Anc!3nt f0rc3 gu!d3s j0urn3y...",
    "R!v3r fl0ws, ch@nge c@rr!3d...",
]

ASCII_ARTS = [
    r"""
    .     .       .  .   . .   .   . .    +  .
      .     .  :     .    .. :. .___---------___.
           .  .   .    .  :.:. _".^ .^ ^.  '.. :"-_. .
        .  :       .  .  .:../:            . .^  :.:\.
            .   . :: +. :.:/: .   .    .        . . .:\
     .  :    .     . _ :::/:               .  ^ .  . .:\
      .. . .   . - : :.:./.                        .  .:\
      .      .     . :..|:                    .  .  ^. .:|
        .       . : : ..||        .                . . !:|
      .     . . . ::. ::\(                           . :)/
     .   .     : . : .:.|. ######              .#######::|
      :.. .  :-  : .:  ::|.#######           ..########:|
     .  .  .  ..  .  .. :\ ########          :######## :/
      .        .+ :: : -.:\ ########       . ########.:/
        .  .+   . . . . :.:\. #######       #######..:/
          :: . . . . ::.:..:.\           .   .   ..:/
       .   .   .  .. :  -::::.\.       | |     . .:/
          .  :  .  .  .-:.":.::.\             ..:/
     .      -.   . . . .: .:::.:.\.           .:/
    .   .   .  :      : ....::_:..:\   ___.  :/
       .   .  .   .:. .. .  .: :.:.:\       :/
         +   .   .   : . ::. :.:. .:.|\  .:/|
         .         +   .  .  ...:: ..|  --.:|
    """,
    r"""
      .     .
    .          .
       *        *
     ' .  .' ' .
    .      *    .
    '*.  . ' ***
      *    .  .
       ' .' '
    """
]

def degrade_text(text, level):
    # Degrade the text by replacing characters with fragments or symbols
    degraded = ""
    for c in text:
        if c.isalpha() and random.random() < level:
            degraded += random.choice("@#$%&*?!")
        elif c.isspace() and random.random() < level / 2:
            degraded += " "
        else:
            degraded += c
    return degraded

def display_ascii_art():
    art = random.choice(ASCII_ARTS)
    print(art)

def main():
    print("Welcome to the Chrono-Entropy Oracle.")
    print("Ask your question, and watch the answer decay over time.\n")

    while True:
        question = input("Your question (or 'quit' to exit): ").strip()
        if question.lower() in ('quit', 'exit'):
            print("Entropy recedes. Farewell.")
            break
        if not question:
            print("The void awaits a proper question.")
            continue

        # Select an initial coherent answer
        answer = random.choice(COHERENT_ANSWERS)
        print("\nOracle answering...\n")
        print(answer)
        display_ascii_art()

        # Simulate decay over time
        for level in [0.1, 0.3, 0.6, 0.9]:
            time.sleep(2)
            degraded_answer = degrade_text(answer, level)
            print("\n" + degraded_answer)
            display_ascii_art()

        # Finally, print surreal fragments
        print("\n" + random.choice(SURREAL_FRAGMENTS))
        display_ascii_art()
        print("\n")

if __name__ == "__main__":
    main()
