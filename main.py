"""
AI Math Tutor
A Khan Academy-inspired mathematics learning application.

Author: Daryn Kabyken
Major: Mathematics, Nazarbayev University

Features:
- Topic-based learning
- Adaptive difficulty
- XP and leveling system
- Streak tracking
- Progress / mastery tracking
- Step-by-step hints
- Immediate feedback
- Khan Academy-inspired learning flow
"""

import random
import math
import json
import os
from dataclasses import dataclass, asdict


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class UserProgress:
    xp: int = 0
    streak: int = 0
    total_questions: int = 0
    correct_answers: int = 0
    algebra_mastery: int = 0
    arithmetic_mastery: int = 0
    geometry_mastery: int = 0
    functions_mastery: int = 0


@dataclass
class Question:
    topic: str
    difficulty: int
    question: str
    answer: float
    explanation: str
    hints: list


# ============================================================
# CONFIGURATION
# ============================================================

SAVE_FILE = "progress.json"

TOPICS = {
    "1": {
        "name": "Arithmetic",
        "description": "Numbers, operations, fractions and percentages"
    },
    "2": {
        "name": "Algebra",
        "description": "Linear equations, expressions and inequalities"
    },
    "3": {
        "name": "Functions",
        "description": "Functions, values and simple modeling"
    },
    "4": {
        "name": "Geometry",
        "description": "Areas, perimeters and basic geometry"
    }
}


# ============================================================
# PROGRESS MANAGEMENT
# ============================================================

def load_progress():
    """Load user progress from a local JSON file."""
    if not os.path.exists(SAVE_FILE):
        return UserProgress()

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return UserProgress(**data)
    except (json.JSONDecodeError, TypeError):
        return UserProgress()


def save_progress(progress):
    """Save user progress locally."""
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(asdict(progress), file, indent=4)


def get_level(xp):
    """Calculate learner level from XP."""
    return (xp // 100) + 1


def get_level_progress(xp):
    """Return XP earned toward the current level."""
    return xp % 100


def get_mastery(progress, topic):
    """Return mastery percentage for a selected topic."""
    mapping = {
        "Arithmetic": progress.arithmetic_mastery,
        "Algebra": progress.algebra_mastery,
        "Functions": progress.functions_mastery,
        "Geometry": progress.geometry_mastery,
    }
    return mapping.get(topic, 0)


def increase_mastery(progress, topic, amount):
    """Increase topic mastery while keeping it between 0 and 100."""
    if topic == "Arithmetic":
        progress.arithmetic_mastery = min(
            100, progress.arithmetic_mastery + amount
        )

    elif topic == "Algebra":
        progress.algebra_mastery = min(
            100, progress.algebra_mastery + amount
        )

    elif topic == "Functions":
        progress.functions_mastery = min(
            100, progress.functions_mastery + amount
        )

    elif topic == "Geometry":
        progress.geometry_mastery = min(
            100, progress.geometry_mastery + amount
        )


# ============================================================
# QUESTION GENERATORS
# ============================================================

def generate_arithmetic(difficulty):
    """Generate arithmetic questions."""
    if difficulty == 1:
        a = random.randint(5, 30)
        b = random.randint(2, 20)

        if random.choice([True, False]):
            return Question(
                topic="Arithmetic",
                difficulty=difficulty,
                question=f"What is {a} + {b}?",
                answer=a + b,
                explanation=f"Add the two numbers: {a} + {b} = {a + b}.",
                hints=[
                    f"Start with {a}.",
                    f"Add {b} more.",
                    f"The result is {a + b}."
                ]
            )

        return Question(
            topic="Arithmetic",
            difficulty=difficulty,
            question=f"What is {a} × {b}?",
            answer=a * b,
            explanation=f"Multiply the numbers: {a} × {b} = {a * b}.",
            hints=[
                f"Think of {b} groups of {a}.",
                f"{a} × {b} is repeated addition.",
                f"The result is {a * b}."
            ]
        )

    elif difficulty == 2:
        denominator = random.choice([2, 4, 5, 10])
        numerator = random.randint(1, denominator - 1)

        return Question(
            topic="Arithmetic",
            difficulty=difficulty,
            question=(
                f"What is {numerator}/{denominator} "
                f"as a decimal?"
            ),
            answer=round(numerator / denominator, 4),
            explanation=(
                f"Divide the numerator by the denominator: "
                f"{numerator} ÷ {denominator} = "
                f"{numerator / denominator}."
            ),
            hints=[
                "A fraction can be written as division.",
                f"Calculate {numerator} ÷ {denominator}.",
                f"The decimal answer is {numerator / denominator}."
            ]
        )

    else:
        price = random.randint(20, 100) * 10
        percent = random.choice([10, 15, 20, 25, 30])

        answer = price * (1 - percent / 100)

        return Question(
            topic="Arithmetic",
            difficulty=difficulty,
            question=(
                f"A product costs {price} KZT and is discounted by "
                f"{percent}%. What is the new price?"
            ),
            answer=round(answer, 2),
            explanation=(
                f"First calculate the discount: "
                f"{price} × {percent}/100 = "
                f"{price * percent / 100:.2f} KZT. "
                f"Then subtract it from the original price: "
                f"{price} - {price * percent / 100:.2f} = {answer:.2f} KZT."
            ),
            hints=[
                f"Find {percent}% of {price}.",
                f"Discount = {price} × {percent}/100.",
                "Subtract the discount from the original price."
            ]
        )


def generate_algebra(difficulty):
    """Generate algebra questions."""
    x = random.randint(1, 15)
    coefficient = random.randint(2, 9)

    if difficulty == 1:
        constant = random.randint(1, 20)
        result = coefficient * x + constant

        return Question(
            topic="Algebra",
            difficulty=difficulty,
            question=f"Solve for x: {coefficient}x + {constant} = {result}",
            answer=x,
            explanation=(
                f"Subtract {constant} from both sides:\n"
                f"{coefficient}x = {result - constant}\n"
                f"Then divide by {coefficient}:\n"
                f"x = {x}"
            ),
            hints=[
                f"First remove {constant} from the left side.",
                f"You should get {coefficient}x = {result - constant}.",
                f"Divide both sides by {coefficient}."
            ]
        )

    elif difficulty == 2:
        constant = random.randint(1, 20)
        result = coefficient * x - constant

        return Question(
            topic="Algebra",
            difficulty=difficulty,
            question=f"Solve for x: {coefficient}x - {constant} = {result}",
            answer=x,
            explanation=(
                f"Add {constant} to both sides:\n"
                f"{coefficient}x = {result + constant}\n"
                f"Now divide by {coefficient}:\n"
                f"x = {x}"
            ),
            hints=[
                f"Add {constant} to both sides.",
                f"You get {coefficient}x = {result + constant}.",
                f"Divide by {coefficient}."
            ]
        )

    else:
        b = random.randint(2, 20)
        result = coefficient * x + b

        return Question(
            topic="Algebra",
            difficulty=difficulty,
            question=f"Solve: {coefficient}x + {b} = {result}",
            answer=x,
            explanation=(
                f"Subtract {b}: "
                f"{coefficient}x = {result - b}\n"
                f"Divide by {coefficient}: x = {x}"
            ),
            hints=[
                "Use inverse operations.",
                f"Subtract {b} from both sides.",
                f"Divide the remaining equation by {coefficient}."
            ]
        )


def generate_functions(difficulty):
    """Generate function questions."""
    a = random.randint(2, 8)
    b = random.randint(-10, 10)
    x = random.randint(-5, 10)

    answer = a * x + b

    return Question(
        topic="Functions",
        difficulty=difficulty,
        question=f"If f(x) = {a}x + ({b}), what is f({x})?",
        answer=answer,
        explanation=(
            f"Substitute x = {x} into the function:\n"
            f"f({x}) = {a}({x}) + ({b})\n"
            f"f({x}) = {answer}"
        ),
        hints=[
            f"Replace x with {x}.",
            f"Calculate {a} × {x}.",
            f"Then add {b}."
        ]
    )


def generate_geometry(difficulty):
    """Generate geometry questions."""
    if random.choice([True, False]):
        width = random.randint(3, 15)
        height = random.randint(3, 15)
        answer = width * height

        return Question(
            topic="Geometry",
            difficulty=difficulty,
            question=(
                f"A rectangle has width {width} cm and "
                f"height {height} cm. What is its area?"
            ),
            answer=answer,
            explanation=(
                f"Rectangle area = width × height.\n"
                f"A = {width} × {height} = {answer} cm²."
            ),
            hints=[
                "Remember the area formula for a rectangle.",
                "Area = width × height.",
                f"Calculate {width} × {height}."
            ]
        )

    radius = random.randint(2, 10)
    answer = round(math.pi * radius ** 2, 2)

    return Question(
        topic="Geometry",
        difficulty=difficulty,
        question=(
            f"A circle has radius {radius} cm. "
            f"Using π ≈ 3.14, what is its area?"
        ),
        answer=round(3.14 * radius ** 2, 2),
        explanation=(
            f"Circle area = πr².\n"
            f"A = 3.14 × {radius}² = {answer} cm²."
        ),
        hints=[
            "The area formula is A = πr².",
            f"First calculate {radius}².",
            "Multiply by approximately 3.14."
        ]
    )


def generate_question(topic, difficulty):
    """Select a generator based on the topic."""
    generators = {
        "Arithmetic": generate_arithmetic,
        "Algebra": generate_algebra,
        "Functions": generate_functions,
        "Geometry": generate_geometry
    }

    return generators[topic](difficulty)


# ============================================================
# LEARNING ENGINE
# ============================================================

def adaptive_difficulty(progress, topic):
    """
    Adapt difficulty based on mastery.

    0–30% mastery -> Level 1
    31–65% mastery -> Level 2
    66–100% mastery -> Level 3
    """
    mastery = get_mastery(progress, topic)

    if mastery <= 30:
        return 1
    elif mastery <= 65:
        return 2
    return 3


def get_xp_reward(difficulty):
    """Return XP reward according to question difficulty."""
    rewards = {
        1: 10,
        2: 15,
        3: 20
    }

    return rewards[difficulty]


def parse_answer(user_input):
    """
    Safely parse numeric answers.

    Accepts:
    10
    10.5
    10,5
    """
    try:
        normalized = user_input.strip().replace(",", ".")
        return float(normalized)
    except ValueError:
        return None


def answers_match(user_answer, correct_answer):
    """Allow small floating-point differences."""
    return math.isclose(
        user_answer,
        correct_answer,
        rel_tol=1e-3,
        abs_tol=0.05
    )


# ============================================================
# UI
# ============================================================

def clear_screen():
    """Clear terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("=" * 65)
    print("                 AI MATH TUTOR")
    print("             Learn • Practice • Master")
    print("=" * 65)


def print_dashboard(progress):
    level = get_level(progress.xp)
    level_progress = get_level_progress(progress.xp)

    accuracy = 0

    if progress.total_questions > 0:
        accuracy = (
            progress.correct_answers /
            progress.total_questions
        ) * 100

    print("\nYOUR LEARNING DASHBOARD")
    print("-" * 65)
    print(f"Level:       {level}")
    print(f"XP:          {progress.xp}")
    print(f"Progress:    {level_progress}/100 XP")
    print(f"Accuracy:    {accuracy:.1f}%")
    print(f"Streak:      {progress.streak} questions")
    print()
    print(f"Arithmetic:  {progress.arithmetic_mastery}%")
    print(f"Algebra:     {progress.algebra_mastery}%")
    print(f"Functions:   {progress.functions_mastery}%")
    print(f"Geometry:    {progress.geometry_mastery}%")
    print("-" * 65)


def choose_topic():
    print("\nCHOOSE A TOPIC")
    print("-" * 65)

    for key, value in TOPICS.items():
        print(
            f"{key}. {value['name']:<12} "
            f"- {value['description']}"
        )

    print("5. Back")

    while True:
        choice = input("\nEnter your choice: ").strip()

        if choice == "5":
            return None

        if choice in TOPICS:
            return TOPICS[choice]["name"]

        print("Please enter a valid option.")


def show_hint(question, hint_number):
    if hint_number <= len(question.hints):
        print(
            f"\n💡 Hint {hint_number}: "
            f"{question.hints[hint_number - 1]}"
        )
    else:
        print("\nNo more hints available.")


# ============================================================
# PRACTICE SESSION
# ============================================================

def practice_session(progress, topic):
    clear_screen()

    difficulty = adaptive_difficulty(progress, topic)

    print_header()

    print(f"\n📚 Topic: {topic}")
    print(f"🎯 Current difficulty: {difficulty}")
    print(f"🏆 Mastery: {get_mastery(progress, topic)}%")

    question_number = 1

    while True:
        question = generate_question(topic, difficulty)

        print("\n" + "-" * 65)
        print(f"Question {question_number}")
        print("-" * 65)
        print(question.question)
        print()

        hint_count = 0

        while True:
            user_input = input(
                "Your answer "
                "(or type 'hint', 'explanation', 'quit'): "
            ).strip()

            if user_input.lower() == "hint":
                hint_count += 1
                show_hint(question, hint_count)
                continue

            if user_input.lower() == "explanation":
                print("\n📖 STEP-BY-STEP EXPLANATION")
                print(question.explanation)
                continue

            if user_input.lower() == "quit":
                save_progress(progress)
                return

            user_answer = parse_answer(user_input)

            if user_answer is None:
                print(
                    "\nPlease enter a number, "
                    "or use 'hint', 'explanation' or 'quit'."
                )
                continue

            progress.total_questions += 1

            if answers_match(user_answer, question.answer):
                reward = get_xp_reward(difficulty)

                # Reduce reward slightly if many hints were used.
                if hint_count == 1:
                    reward -= 2
                elif hint_count >= 2:
                    reward -= 5

                reward = max(reward, 5)

                progress.xp += reward
                progress.correct_answers += 1
                progress.streak += 1

                # Increase mastery.
                mastery_gain = 5 if hint_count == 0 else 3
                increase_mastery(progress, topic, mastery_gain)

                print("\n✅ Correct!")
                print(f"🌟 +{reward} XP")
                print(
                    f"🔥 Streak: {progress.streak}"
                )

                new_level = get_level(progress.xp)

                if progress.xp % 100 < reward:
                    print(
                        f"\n🎉 LEVEL UP! You are now Level {new_level}!"
                    )

                print(
                    f"📈 {topic} mastery: "
                    f"{get_mastery(progress, topic)}%"
                )

                save_progress(progress)

                break

            else:
                progress.streak = 0

                print("\n❌ Not quite.")

                print(
                    f"Try again, or type 'hint' "
                    f"for a guided explanation."
                )

                save_progress(progress)

        question_number += 1

        print("\nWhat would you like to do?")
        print("1. Next question")
        print("2. Return to dashboard")

        choice = input("\nChoice: ").strip()

        if choice == "2":
            save_progress(progress)
            return

        # Adaptive difficulty update after every question.
        difficulty = adaptive_difficulty(progress, topic)


# ============================================================
# STUDY RECOMMENDATIONS
# ============================================================

def study_recommendation(progress):
    """Recommend what the learner should study next."""
    mastery = {
        "Arithmetic": progress.arithmetic_mastery,
        "Algebra": progress.algebra_mastery,
        "Functions": progress.functions_mastery,
        "Geometry": progress.geometry_mastery
    }

    weakest_topic = min(mastery, key=mastery.get)

    print("\n🤖 PERSONALIZED RECOMMENDATION")
    print("-" * 65)

    print(
        f"Your weakest topic is currently "
        f"**{weakest_topic}** ({mastery[weakest_topic]}% mastery)."
    )

    if mastery[weakest_topic] < 30:
        print(
            "Recommendation: Start with the fundamentals "
            "and focus on understanding each step."
        )

    elif mastery[weakest_topic] < 70:
        print(
            "Recommendation: Practice medium-difficulty "
            "problems to strengthen your understanding."
        )

    else:
        print(
            "Recommendation: Challenge yourself with "
            "advanced problems."
        )

    print("-" * 65)


# ============================================================
# MAIN MENU
# ============================================================

def main():
    progress = load_progress()

    while True:
        clear_screen()
        print_header()

        print_dashboard(progress)

        print("\nMAIN MENU")
        print("-" * 65)
        print("1. Start Practice")
        print("2. View Progress")
        print("3. Get AI Learning Recommendation")
        print("4. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            topic = choose_topic()

            if topic:
                practice_session(progress, topic)

        elif choice == "2":
            clear_screen()
            print_header()
            print_dashboard(progress)

            input("\nPress Enter to return...")

        elif choice == "3":
            clear_screen()
            print_header()
            study_recommendation(progress)

            input("\nPress Enter to return...")

        elif choice == "4":
            save_progress(progress)

            print("\n")
            print("=" * 65)
            print("Keep learning. Keep growing. 🚀")
            print("=" * 65)
            break

        else:
            print("\nInvalid choice.")
            input("Press Enter to continue...")


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
