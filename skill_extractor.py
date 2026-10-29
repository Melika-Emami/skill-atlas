# importing required classes
from pypdf import PdfReader
import re

skill_keywords = {
    "FIFO buffering": ["fifo", "first-in-first-out"],
    "Statistical analysis": ["standard deviation"],
    "Data aggregation": ["aggregation", "aggregate"],
    "Symbolic Aggregate Approximation": ["symbolic aggregate approximation", "sax"],
}


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

            match = re.search(pattern, text, flags=re.IGNORECASE)

            if match:
                each_skill["matched_phrases"].append(
                    {
                        "keyword": phrase,
                        "matched_text": match.group(),
                        "start": match.start(),
                        "end": match.end(),
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
    results = extract_skills_from_pdf("assignment", skill_keywords)

    for result in results:
        print(result)
