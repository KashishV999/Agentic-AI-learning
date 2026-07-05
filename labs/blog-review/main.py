import os
import sys
import base64
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# -----------------------------------------------------------------------------
# Environment Configuration
# -----------------------------------------------------------------------------

# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# -----------------------------------------------------------------------------
# File Utilities
# -----------------------------------------------------------------------------

def get_file_contents(path: str, description: str) -> str:
    """
    Read a file and return its contents.

    Args:
        path: Path to the file.
        description: Human-readable description used in error messages.

    Returns:
        File contents as a string.

    Exits:
        Program exits if the file cannot be read.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    except FileNotFoundError:
        print(f"❌ Error: {description} not found: {path}")
        sys.exit(1)

    except Exception as err:
        print(f"❌ Error reading {description}: {path}")
        print(f"   {err}")
        sys.exit(1)


def get_folder_content(folder_path: str) -> str:
    """
    Read all files in a folder and combine them into a single string.

    Each file is wrapped in an XML-like tag so the LLM can identify
    the original file name.

    Args:
        folder_path: Folder containing text files.

    Returns:
        Combined content from all files.
    """
    content = ""

    try:
        folder = Path(folder_path)

        if not folder.exists():
            print(f"⚠ Warning: Folder not found: {folder_path}")
            return content

        for file_path in sorted(folder.glob("*")):
            if not file_path.is_file():
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()

                content += (
                    f"\n<file name='{file_path.name}'>\n"
                    f"{file_content}\n"
                    f"</file>\n"
                )

                print(f"✓ Loaded file: {file_path.name}")

            except Exception as e:
                print(
                    f"⚠ Warning: Could not load file "
                    f"{file_path.name}: {e}"
                )

    except Exception as e:
        print(f"⚠ Warning: Error scanning folder for content: {e}")

    return content


def get_images_from_folder(folder_path: str) -> list:
    """
    Load images from a folder and encode them as Base64.

    Args:
        folder_path: Folder containing image files.

    Returns:
        List of image payloads compatible with multimodal LLM APIs.
    """
    images = []

    media_type_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }

    try:
        folder = Path(folder_path)

        if not folder.exists():
            return images

        for image_ext in ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp"]:
            for image_path in sorted(folder.glob(image_ext)):
                try:
                    with open(image_path, "rb") as f:
                        image_data = base64.standard_b64encode(
                            f.read()
                        ).decode("utf-8")

                    images.append(
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type_map.get(
                                    image_path.suffix.lower(),
                                    "image/png",
                                ),
                                "data": image_data,
                            },
                        }
                    )

                    print(f"✓ Loaded image: {image_path.name}")

                except Exception as e:
                    print(
                        f"⚠ Warning: Could not load image "
                        f"{image_path.name}: {e}"
                    )

    except Exception as e:
        print(f"⚠ Warning: Error scanning folder for images: {e}")

    return images


# -----------------------------------------------------------------------------
# OpenRouter / LLM Integration
# -----------------------------------------------------------------------------

def chat_completion():
    """
    Send onboarding documentation to the LLM for review.

    Returns:
        OpenRouter completion response object.
    """
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    # Usage
    system_prompt = get_file_contents(
        "SYSTEM_PROMPT.md",
        "System prompt file"
    )

    # major_issues_prompt = get_file_contents(
    #     "MAJOR_ISSUES.md",
    #     "Major issues prompt file",
    # )

    blog_content = get_file_contents(
        "Blog.md",
        "Blogs file"
    )

    # images = get_images_from_folder(
    #     "blog/knative-headlamp-plugin"
    # )

    # function : get the content of the folder
    # : ../contributor-site/content/en/docs/onboarding

    # files_content = get_folder_content(
    #     "../contributor-site/content/en/docs/onboarding"
    # )

    # print(files_content)

    # Build user message content with text and images
    user_content = [
        {
            "type": "text",
            "text": (
                "Here is the blog:\n"
                f"<blog>\n{blog_content}\n</blog>"
            ),
        }
    ]

    # Add images to the message
    # user_content.extend(images)

    completion = client.chat.completions.create(
        model="anthropic/claude-sonnet-4.6",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": blog_content
            },
        ],
    )

    return completion


# -----------------------------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------------------------

def main():
    """
    Validate configuration and run the review workflow.
    """
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found")
        sys.exit(1)

    print("OPENROUTER_API_KEY found successfully!")

    completion_choice = (
        chat_completion()
        .choices[0]
        .message.content
    )

    print("Blog Review:\n")
    print(completion_choice)


if __name__ == "__main__":
    main()