# image_dataset_builder.py

import os
import time
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from ddgs import DDGS
import matplotlib.pyplot as plt

def create_dataset_image(query: str, num_images: int = 10, convert_to_jpg: bool = True):
    
    # Create a directory for the dataset based on the query
    folder = f"dataset/{query.replace(' ', '_')}"
    os.makedirs(folder, exist_ok=True)

    image_paths = []
    print(f"\nSearching for images: '{query}' ({num_images} images)...")

    with DDGS() as ddgs:
        try:
            # Request more results than needed to compensate for invalid or failed images
            results = ddgs.images(query, max_results=num_images * 5) 
            image_index = 1
            error_count = 0
            skipped_count = 0

            for result in results:
                if len(image_paths) >= num_images:
                    break  # Stop when the desired number of images has been collected

                url = result.get('image')
                if not url:
                    continue  # Skip if no image URL is present

                try:
                    # Download the image
                    response = requests.get(url, timeout=10)
                    img = Image.open(BytesIO(response.content))

                    # Validate supported image formats
                    if img.format not in ['JPEG', 'JPG', 'PNG', 'WEBP']:
                        raise ValueError(f"Unsupported image format: {img.format}")

                    # Convert image to JPG if requested
                    if convert_to_jpg:
                        img = img.convert("RGB")
                        ext = "jpg"
                    else:
                        ext = img.format.lower()

                    # Build the file path and save the image
                    filename = f"{query.replace(' ', '_')}_{image_index}.{ext}"
                    filepath = os.path.join(folder, filename)
                    img.save(filepath)

                    image_paths.append(filepath)
                    print(f"✅ Saved: {filepath}")
                    image_index += 1

                # Handle unsupported or unreadable images
                except (UnidentifiedImageError, ValueError) as e:
                    skipped_count += 1
                    print(f"❌ Skipped (invalid image) from {url[:50]}...: {e}")
                # Handle all other exceptions (timeouts, etc.)
                except Exception as e:
                    error_count += 1
                    print(f"❌ Error with image from {url[:50]}...: {e}")

        # Handle search failure (e.g. DuckDuckGo unreachable or rate limited)
        except Exception as e:
            print(f"❌ DuckDuckGo search failed: {e}")
            return

    if not image_paths:
        print("No valid images were downloaded.")
        return

    # Print a summary for the current query
    print(f"\nSummary for '{query}':")
    print(f"   ✅ {len(image_paths)} images saved")
    print(f"   ❌ {error_count} download errors")
    print(f"   ❌ {skipped_count} skipped (invalid format or unreadable)")

    # Show the first and last downloaded images
    try:
        print("\nDisplaying first and last downloaded images...")
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].imshow(Image.open(image_paths[0]))
        ax[0].set_title("First Image")
        ax[0].axis("off")

        ax[1].imshow(Image.open(image_paths[-1]))
        ax[1].set_title("Last Image")
        ax[1].axis("off")

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Could not display images: {e}")

def main():
    print("=== Image Dataset Builder ===\n")
    
    # Ask user to enter search queries separated by commas
    queries = input("Enter your search queries (comma-separated): ").split(",")
    queries = [q.strip() for q in queries if q.strip()]

    # Ask user how many images per query
    try:
        num_images = int(input("How many images per query? (default = 10): ") or "10")
    except ValueError:
        print("Invalid number, defaulting to 10 images.")
        num_images = 10

    # Ask if images should be converted to JPG
    convert_choice = input("Convert all images to JPG? (y/n): ").lower() or "y"
    convert_to_jpg = convert_choice == "y"

    # Loop over each search query
    for query in queries:
        create_dataset_image(query, num_images, convert_to_jpg)
        time.sleep(2)  # Wait to reduce the chance of hitting rate limits

    print("\n✅ All datasets completed.")

if __name__ == "__main__":
    main()
