import random
import anthropic
import os

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def generate_subject_and_items(subject=None):
    number_of_items = random.randint(3, 6)
    system_prompt = "You are an AI assistant helping to generate content for a Family Feud game."
    if subject:
        human_prompt = f"Generate {number_of_items} items related to the subject '{subject}' for a Family Feud game, ranked by popularity. Format the response as 'Items: 1. [item1], 2. [item2], 3. [item3], 4. [item4], 5. [item5], 6. [item6]'"
    else:
        human_prompt = f"Generate a subject for a Family Feud game and {number_of_items} items related to that subject, ranked by popularity. Format the response as 'Subject: [subject]\nItems: 1. [item1], 2. [item2], 3. [item3], 4. [item4], 5. [item5], 6. [item6]'"
    
    messages = [
        {
            "role": "user",
            "content": human_prompt
        }
    ]
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=messages,
        max_tokens=300,
        system=system_prompt
    )
    
    result = [line for line in response.content[0].text.strip().split('\n') if line]
    print(result)
    if subject:
        items = [item.split('. ')[1] for item in result[0][result[0].index(":"):].split(', ')]
        return subject, items
    else:
        subject = result[0].split(': ')[1]
        items = [item.split('. ')[1] for item in result[1][result[1].index(":"):].split(', ')]
        return subject, items
    
def judge_guess(guess, items):
    system_prompt = "You are an AI assistant judging if an item is contained in a list. The item does not need to be an exact match. Format the response as 'Yes [matching-item]' or 'No'"
    human_prompt = f"Does the list {items} contain '{guess}'?"

    messages = [
        {
            "role": "user",
            "content": human_prompt
        }
    ]

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=messages,
        max_tokens=300,
        system=system_prompt
    )

    print(response.content[0].text.strip().lower())
    return response.content[0].text.strip().lower()

def assign_scores(items):
    base_score = 100 // len(items)
    scores = [base_score] * len(items)
    remaining_points = 100 - sum(scores)
    
    for i in range(remaining_points):
        random_index = random.randint(0, len(items) - 1)
        scores[random_index] += 1
    
    return dict(zip(items, scores))

def play_game():
    print("Welcome to Family Feud!")
    user_subject = input("Enter a subject (or press Enter for a random subject): ").strip()
    
    if user_subject:
        subject, items = generate_subject_and_items(user_subject)
    else:
        subject, items = generate_subject_and_items()
    
    item_scores = assign_scores(items)
    
    print(f"The subject is: {subject}")
    print("Try to guess the top answers!")
    
    guessed_items = set()
    wrong_guesses = 0
    total_score = 0
    
    try:
        while len(guessed_items) < len(items) and wrong_guesses < 3:
            guess = input("Enter your guess: ").strip().lower().strip()
            judge = judge_guess(guess, items)
            if judge.startswith("y"):
                item_match = judge[judge.index('[')+1:judge.index(']')]
                item = next(item for item in items if item.lower().strip() == item_match.lower().strip())
                if item not in guessed_items:
                    guessed_items.add(item)
                    score = item_scores[item]
                    total_score += score
                    print(f"Correct! '{item}' is worth {score} points.")
                    print(f"Your total score: {total_score}")
                else:
                    print("You already guessed that item!")
            else:
                wrong_guesses += 1
                print(f"Sorry, that's not on the board. Wrong guesses: {wrong_guesses}/3")
        
        print("\nGame Over!")
        if wrong_guesses == 3:
            print("You've used all your wrong guesses. Here are the answers:")
        else:
            print("Congratulations! You've guessed all the items. Here are the final results:")
    except Exception as e:
        print("something happened")
        print(e)
    
    for item, score in item_scores.items():
        print(f"{item}: {score} points")
    
    print(f"Your final score: {total_score}")

if __name__ == "__main__":
    play_game()