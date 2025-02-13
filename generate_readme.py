import csv
from collections import defaultdict
import urllib.parse

# Define start and stop markers
START_MARKER = "<!-- START_GENERATED_CONTENT -->"
STOP_MARKER = "<!-- END_GENERATED_CONTENT -->"

def generate_toc(categories):
    toc = "## Table of Contents\n\n"
    for category in sorted(categories.keys()):
        link = category.lower().replace(' ', '-').replace('&', '').replace(':', '').replace('(', '').replace(')', '')
        toc += f"- [{category}](#{link})\n"
    return toc + "\n"

def generate_readme(csv_file, readme_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        subreddits = list(reader)

    if not subreddits:
        print("subreddits.csv is empty or has incorrect headers. Please populate it with data.")
        return

    # Group subreddits by category
    categories = defaultdict(list)
    category_descriptions = {}
    for subreddit in subreddits:
        categories[subreddit['cat']].append(subreddit)
        if subreddit['cat'] not in category_descriptions and subreddit.get('my_notes'):
            category_descriptions[subreddit['cat']] = subreddit['my_notes']

    # Sort subreddits within each category
    for category in categories:
        categories[category].sort(key=lambda x: x['subreddit'].lower())

    # Read the existing README content
    with open(readme_file, 'r') as f:
        readme_content = f.read()

    # Find the start and stop markers
    start_index = readme_content.find(START_MARKER)
    stop_index = readme_content.find(STOP_MARKER)

    # If markers are not found, add them
    if start_index == -1 or stop_index == -1:
        start_index = readme_content.find('# Awesome AI Subreddits')
        if start_index == -1:
            print("Unable to find a suitable location to insert generated content.")
            return
        stop_index = start_index

    # Generate the new content
    new_content = f"{START_MARKER}\n\n"
    new_content += '# Awesome AI Subreddits\n\nA curated list of awesome AI-related subreddits.\n\n'
    new_content += generate_toc(categories)

    # Generate content for each category
    for category in sorted(categories.keys()):
        subs = categories[category]
        new_content += f'## {category}\n\n'
        if category in category_descriptions:
            new_content += f'{category_descriptions[category]}\n\n'
        for subreddit in subs:
            subreddit_name = subreddit['subreddit'].replace('r/', '')
            link = subreddit['subreddit_url']
            description = subreddit['sub_description']
            
            # Create static badge using shields.io with URL-safe encoding
            encoded_name = urllib.parse.quote(subreddit_name)
            badge = f'[![View Subreddit](https://img.shields.io/badge/View-{encoded_name}-orange)]({link})'
            
            new_content += f'### {subreddit_name}\n\n'
            if description:
                new_content += f'{description}\n\n'
            new_content += f'{badge}\n\n'

    new_content += f"\n{STOP_MARKER}\n\n"

    # Add instructions on how to update the list
    new_content += '## How to Update the List\n\n'
    new_content += '1. Edit the `subreddits.csv` file to add, remove, or modify subreddits.\n'
    new_content += '2. Run `python generate_readme.py` to regenerate the list.\n\n'

    # Find the "How to Update the List" section in the new content
    how_to_update_index = new_content.find('## How to Update the List')
    if how_to_update_index == -1:
        how_to_update_index = len(new_content)

    # Find the Author section in the existing content
    author_section_index = readme_content.find('## Author')
    if author_section_index == -1:
        author_section_index = len(readme_content)

    # Combine the parts
    updated_content = (
        readme_content[:start_index] +
        new_content[:how_to_update_index] +
        '\n\n' + readme_content[author_section_index:]
    )

    # Write the updated content back to the README file
    with open(readme_file, 'w') as f:
        f.write(updated_content)

if __name__ == "__main__":
    generate_readme('subreddits.csv', 'README.md')