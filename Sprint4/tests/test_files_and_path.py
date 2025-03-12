from pathlib import Path
from unittest import mock

from Sprint4.utils.file_and_path_utils import (
    save_file,
    clean_markdown,
    convert_markdown_to_html,
    convert_md_to_pdf
)


# Test for save_file function
def test_save_file():
    content = "Sample resume content"
    file_path = Path("generated_files/markdowns/john_doe_resume.md")

    # Mocking the file write operation
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        save_file(content, file_path)
        mock_file.assert_called_once_with(file_path, "w")
        mock_file().write.assert_called_once_with(content)


# Test for clean_markdown function
def test_clean_markdown():
    raw_md_content = """
    This is a `inline code` example.

    ```
    This is a code block
    ```
    """

    expected_clean_content = """
    This is a  example.

    
    """
    cleaned_content = clean_markdown(raw_md_content)
    assert cleaned_content == expected_clean_content


# Test for convert_markdown_to_html function
def test_convert_markdown_to_html():
    md_content = "# This is a header\n\nThis is content"
    expected_html_content = "<h1>This is a header</h1>\n<p>This is content</p>"

    html_content = convert_markdown_to_html(md_content)
    assert html_content == expected_html_content


# Test for convert_md_to_pdf function
def test_convert_md_to_pdf():
    md_file = "test_resume.md"
    pdf_file = "generated_files/pdfs/test_resume.pdf"

    # Mocking file read and file write operations
    with mock.patch("builtins.open", mock.mock_open(read_data="Sample Markdown")):
        with mock.patch("Sprint4.utils.file_and_path_utils.clean_markdown", return_value="Cleaned Markdown"):
            with mock.patch("Sprint4.utils.file_and_path_utils.convert_markdown_to_html", return_value="<h1>HTML</h1>"):
                with mock.patch("xhtml2pdf.pisa.CreatePDF") as mock_create_pdf:
                    mock_create_pdf.return_value.err = 0  # Mocking success

                    # Test the function
                    convert_md_to_pdf(md_file, pdf_file)
                    mock_create_pdf.assert_called_once_with("<h1>HTML</h1>", dest=mock.ANY)
