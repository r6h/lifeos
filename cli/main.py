from soul_engine.extractor import extract_profile_from_input, save_profile_to_json
from soul_engine.model import SoulProfile

def ask_user_questions() -> str:
    questions = [
        ("background_context", "Before we begin, tell me a bit about where you are in life — age, background, what you're doing now."),
        ("core values", "What are some principles or values that you care deeply about in life?"),
        ("motivations", "What drives you to do what you do? What goals or dreams keep you going?"),
        ("fears", "What are some fears or doubts you have about your future or capabilities?"),
        ("skills", "What skills or strengths do you currently have, or want to develop?"),
        ("interests", "What topics, hobbies, or ideas fascinate you deeply?"),
        ("worldview", "How do you see the world? What beliefs or philosophies shape your thinking?"),
        ("notes", "Anything else you'd like to share that doesn’t fit the previous questions?")
    ]

    print("\n🧠 Welcome to the Soul Engine Interactive Mode\n")
    print("Please answer the following questions to help us build your Soul Profile.\n")

    # Initialize an empty string to store the combined input
    # Iterate through the questions and collect user input
    combined_input = ""
    for field, question in questions:
        print(f"\n👉 {question}")
        answer = input("> ").strip()
        if answer:
            combined_input += f"{field.capitalize()}: {answer}\n"

    return combined_input

# MAIN STARTER
# This is the main entry point for the CLI application.
def main():
    user_input = ask_user_questions()

    try: 
        profile: SoulProfile = extract_profile_from_input(user_input)
        print("\n✅ Generated Soul Profile:\n")
        print(profile.model_dump_json(indent=2))
        save_profile_to_json(profile)
        print("\n✅ Profile saved successfully!")
    except Exception as e:
        print(f"\n❌ Failed to generate profile: {e}")

if __name__ == "__main__":
    main()