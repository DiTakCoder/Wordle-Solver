def load_words(filename="words.txt"):
    """
    Load and return a list of all 5-letter words from the given file,
    converting each to lowercase so the rest of the code works correctly.
    """
    with open(filename, "r") as f:
        return [line.strip().lower() for line in f if len(line.strip()) == 5]

def evaluate_guess(guess, secret):
    """
    Given a guess and a secret, return feedback as a list of 5 integers:
      2 → green  (correct letter, correct position)
      1 → yellow (letter is in secret but wrong position)
      0 → gray   (letter not in secret at all)

    Implements “consume‐once” logic so letters aren’t double‐counted.
    """
    feedback = [0] * 5
    secret_chars = list(secret)
    # First pass: mark greens (2) and remove from consideration
    for i in range(5):
        if guess[i] == secret[i]:
            feedback[i] = 2
            secret_chars[i] = None
    # Second pass: mark yellows (1) if letter exists elsewhere
    for i in range(5):
        if feedback[i] == 0 and guess[i] in secret_chars:
            feedback[i] = 1
            secret_chars[secret_chars.index(guess[i])] = None
    return feedback

def feedback_string_to_list(fb_str):
    """
    Convert a 5-character feedback string ('g', 'y', 'b') into a list [0..2]:
      'g' → 2, 'y' → 1, 'b' → 0.
    Raises ValueError if fb_str has invalid length or characters.
    """
    fb_str = fb_str.strip().lower()
    if len(fb_str) != 5 or any(ch not in "gyb" for ch in fb_str):
        raise ValueError("Feedback must be exactly 5 chars from {'g','y','b'}.")
    return [ {"g":2, "y":1, "b":0}[ch] for ch in fb_str ]

def format_feedback(guess, feedback):
    """
    Turn feedback list [0/1/2,...] into emojis:
      2 → 🟩, 1 → 🟨, 0 → ⬜
    """
    symbols = {2:"🟩", 1:"🟨", 0:"⬜"}
    return "".join(symbols[f] for f in feedback) + "   (" + guess + ")"

def filter_candidates(cands, last_guess, last_fb):
    """
    From the current list of candidate words, keep only those words that would
    produce the same feedback if 'last_guess' were compared to them.
    """
    out = []
    for w in cands:
        if evaluate_guess(last_guess, w) == last_fb:
            out.append(w)
    return out

def pick_smart(cands):
    """
    From the candidate list, pick the word containing the most vowels (a, e, i, o, u).
    If multiple words tie, break ties by a position‐frequency score: build a
    frequency table of letters by position across cands, then score each word
    by summing freq[pos][letter], counting each letter only once per word.
    Return the highest‐scoring word.
    """
    VOWELS = set("aeiou")
    # 1) Count number of vowels in each candidate
    vowel_counts = [(sum(1 for ch in w if ch in VOWELS), w) for w in cands]
    # Determine the max vowel count
    max_vowel = max(count for count, _ in vowel_counts)
    # Filter words that have that max vowel count
    vowel_heavy = [w for count, w in vowel_counts if count == max_vowel]

    # If only one word has the max vowel count, return it
    if len(vowel_heavy) == 1:
        return vowel_heavy[0]

    # Otherwise, build position‐frequency among all candidates
    freq = [dict.fromkeys("abcdefghijklmnopqrstuvwxyz", 0) for _ in range(5)]
    for w in cands:
        for i, ch in enumerate(w):
            freq[i][ch] += 1

    # Score each vowel_heavy word by summing freq[i][ch], counting each letter only once
    best_score = -1
    best_word = vowel_heavy[0]
    for w in vowel_heavy:
        seen = set()
        score = 0
        for i, ch in enumerate(w):
            if ch in seen:
                continue
            seen.add(ch)
            score += freq[i][ch]
        if score > best_score:
            best_score = score
            best_word = w

    return best_word

def interactive_solve():
    word_list = load_words("words.txt")
    candidates = word_list.copy()

    print("\n===== Interactive Wordle Solver (Vowel‐First Heuristic) =====")
    print("Each round, it chooses the candidate with the most vowels (tie‐broken by letter‐frequency).")
    print("After you enter that guess in Wordle, copy the feedback here as 'g' (green), 'y' (yellow), or 'b' (gray).")
    print("Type 'exit' to quit.\n")

    round_num = 1
    while True:
        if not candidates:
            print("❌ No candidates left—check your feedback and word list!")
            return

        guess = pick_smart(candidates)
        print(f"Round {round_num}:  Suggesting →  {guess.upper()}")
        fb_input = input("Feedback (5 chars, g/y/b): ").strip().lower()

        if fb_input == "exit":
            print("Exiting solver.")
            return

        try:
            feedback = feedback_string_to_list(fb_input)
        except ValueError as e:
            print("  ❗", e)
            print("  Please re‐enter feedback using exactly 5 letters from 'g','y','b'.\n")
            continue

        print("   You entered:", format_feedback(guess, feedback), "\n")

        if feedback == [2, 2, 2, 2, 2]:
            print(f"🎉 Solved in {round_num} rounds! The word is '{guess.upper()}'.\n")
            return

        candidates = filter_candidates(candidates, guess, feedback)
        print(f"   → {len(candidates)} possible words remain.\n")
        round_num += 1

if __name__ == "__main__":
    interactive_solve()
