# importing required classes
from pypdf import PdfReader
import re
import json
from pathlib import Path

skill_keywords = {
    "FIFO buffering": ["fifo", "first-in-first-out"],
    "Statistical analysis": ["standard deviation"],
    "Data aggregation": ["aggregation", "aggregate"],
    "Symbolic Aggregate Approximation": ["symbolic aggregate approximation", "sax"],
}

context_chars = 150


def clean_text(text: str) -> str:
    text = text.replace("\u00a0", " ")

    # Remove leading and trailing whitespace from each line.
    text = "\n".join(line.strip() for line in text.splitlines())

    # Reduce repeated blank lines to one blank line
    text = re.sub(r"\n(?:[ \t]*\n)+", "\n\n", text)

    return text


def read_pdf(file_name: str) -> list[dict]:
    # creating a pdf reader object
    reader = PdfReader(r"examples/{}.pdf".format(file_name))

    pdf_pages = []
    for i, page in enumerate(reader.pages):
        # creating a page object
        raw = page.extract_text()
        clean = clean_text(raw)
        pdf_pages.append({"page_number": i + 1, "raw_text": raw, "clean_text": clean})

    return pdf_pages


def find_skill_keywords(
    text: str,
    skill_keywords: dict[str, list[str]],
) -> list[dict]:
    found_skills = []

    for key, values in skill_keywords.items():
        each_skill = {"skill": key, "matched_phrases": []}

        for phrase in values:
            words = phrase.split()
            pattern = r"\b" + r"\s+".join(re.escape(word) for word in words) + r"\b"

            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                excerpt_start = max(0, match.start() - context_chars)
                excerpt_end = min(len(text), match.end() + context_chars)

                each_skill["matched_phrases"].append(
                    {
                        "keyword": phrase,
                        "matched_text": match.group(),
                        "start": match.start(),
                        "end": match.end(),
                        "excerpt": text[excerpt_start:excerpt_end],
                        "excerpt_start": excerpt_start,
                        "excerpt_end": excerpt_end,
                    }
                )

        if each_skill["matched_phrases"]:
            found_skills.append(each_skill)

    return found_skills


def extract_skills_from_pdf(
    file_name: str,
    skill_keywords: dict[str, list[str]],
) -> list[dict]:
    pdf_pages = read_pdf(file_name)
    results = []

    for page in pdf_pages:
        found_skills = find_skill_keywords(page["clean_text"], skill_keywords)

        for skill in found_skills:
            skill["page_number"] = page["page_number"]

        results.extend(found_skills)

    return results


if __name__ == "__main__":
    file_name = "assignment"
    results = extract_skills_from_pdf(file_name, skill_keywords)

    final_results = {
        "source_file": f"{file_name}.pdf",
        "skills": results,
    }

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / f"{file_name}.json").open("w", encoding="utf-8") as fp:
        json.dump(final_results, fp, ensure_ascii=False, indent=4)

    # print(results[0])
    # for result in results:
    #     print(result)
