import os
import re
import shutil
from ebooklib import epub, ITEM_STYLE

NEW_MARGIN = "0 !important"
NEW_PADDING = "0 !important"

def replace_margins_and_padding_in_css(css_content):
    # Replace margin properties
    css_content = re.sub(
        r'margin(?:-top|-bottom|-left|-right)?\s*:\s*[0-9.]+\s*(?:px|em|rem|%)?\s*;',
        f'margin: {NEW_MARGIN};',
        css_content,
        flags=re.IGNORECASE
    )
    # Replace padding properties
    css_content = re.sub(
        r'padding(?:-top|-bottom|-left|-right)?\s*:\s*[0-9.]+\s*(?:px|em|rem|%)?\s*;',
        f'padding: {NEW_PADDING};',
        css_content,
        flags=re.IGNORECASE
    )
    return css_content

def process_epub(epub_path, output_folder):
    epub_filename = os.path.basename(epub_path)
    output_path = os.path.join(output_folder, epub_filename)

    # Load the EPUB file
    book = epub.read_epub(epub_path)

    # Iterate over all CSS files in the EPUB
    for item in book.get_items_of_type(ITEM_STYLE):
        css_content = item.get_content().decode('utf-8')
        new_css_content = replace_margins_and_padding_in_css(css_content)
        item.set_content(new_css_content.encode('utf-8'))
        print(f"Processed CSS: {item.file_name}")

    # Save the modified EPUB to the output folder
    epub.write_epub(output_path, book, {})

    print(f"Processed EPUB saved to: {output_path}")

def main():
    epub_folder = "./input_files"  #Ensure this points to your input_files subfolder
    output_folder = "./processed_epubs"
    os.makedirs(output_folder, exist_ok=True)

    try:
        epub_files = [
            os.path.join(epub_folder, f)
            for f in os.listdir(epub_folder)
            if f.lower().endswith('.epub')
        ]
    except FileNotFoundError:
        print(f"The folder '{epub_folder}' does not exist.")
        return

    if not epub_files:
        print("No EPUB files found in the input_files directory.")
        return

    for epub_file in epub_files:
        try:
            process_epub(epub_file, output_folder)
        except Exception as e:
            print(f"Failed to process {epub_file}: {e}")

if __name__ == "__main__":
    main()

