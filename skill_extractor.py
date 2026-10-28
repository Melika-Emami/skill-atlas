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
    normalised_text = text.casefold()

    for key, values in skill_keywords.items():
        each_skill = {"skill": key, "matched_phrases": []}

        for phrase in values:
            if phrase.casefold() in normalised_text:
                each_skill["matched_phrases"].append(phrase)

        if each_skill["matched_phrases"]:
            found_skills.append(each_skill)

    return found_skills


if __name__ == "__main__":
    pdf_pages = read_pdf("assignment")
    # print(pdf_pages[0]["clean_text"])
    found_skills = find_skill_keywords(pdf_pages[0]["clean_text"], skill_keywords)
    print(found_skills)
