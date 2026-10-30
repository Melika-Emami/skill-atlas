import json
from pathlib import Path


def ask_for_review() -> dict[str, str]:
    options = {
        "1": "relevant",
        "2": "irrelevant",
        "3": "uncertain",
    }

    print("Does this passage support the skill's relevance?")
    print("1. Relevant")
    print("2. Irrelevant")
    print("3. Uncertain")

    while True:
        choice = input("Your choice (1/2/3): ").strip()

        if choice in options:
            break

        print("Please enter 1, 2 or 3.")

    note = input("Reason or note (optional): ").strip()

    return {
        "status": options[choice],
        "note": note,
    }


def display_skill_evidence(
    source_file: str,
    skill_name: str,
    page_number: int,
    match: dict,
) -> None:
    print("-" * 60)
    print(f"Source: {source_file}")
    print(f"Skill: {skill_name}")
    print(f"Page: {page_number}")
    print(f"Keyword: {match['keyword']}")
    print(f"Matched text: {match['matched_text']}")
    print(f"Location: {match['start']}–{match['end']} (end exclusive)")
    print("\nEvidence:")
    print(match["excerpt"])
    print()


import json
from pathlib import Path

# Keep display_skill_evidence() and ask_for_review() above this block.

if __name__ == "__main__":
    file_name = "assignment"
    input_path = Path("outputs") / f"{file_name}.json"
    output_path = Path("outputs") / f"{file_name}_reviewed.json"

    # Resume from previous reviews if available.
    load_path = output_path if output_path.exists() else input_path

    with load_path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)

    for skill in data["skills"]:
        for match in skill["matched_phrases"]:
            # Skip matches already reviewed.
            if "review" in match:
                continue

            display_skill_evidence(
                source_file=data["source_file"],
                skill_name=skill["skill"],
                page_number=skill["page_number"],
                match=match,
            )

            match["review"] = ask_for_review()

            # Save after each judgement to preserve progress.
            with output_path.open("w", encoding="utf-8") as fp:
                json.dump(data, fp, ensure_ascii=False, indent=4)

    print(f"Review complete. Results saved to {output_path}")
