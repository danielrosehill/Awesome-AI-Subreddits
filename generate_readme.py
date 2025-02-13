import csv
from collections import defaultdict

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

    markdown_list = '# Awesome AI Subreddits\n\nA curated list of awesome AI-related subreddits.\n\n'
    
    # Add Table of Contents
    markdown_list += generate_toc(categories)

    # Generate content for each category
    for category in sorted(categories.keys()):
        subs = categories[category]
        markdown_list += f'## {category}\n\n'
        if category in category_descriptions:
            markdown_list += f'{category_descriptions[category]}\n\n'
        for subreddit in subs:
            subreddit_name = subreddit['subreddit']
            link = subreddit['subreddit_url']
            description = subreddit['sub_description']
            badge = f'[![View Subreddit](https://img.shields.io/badge/View-Subreddit-orange)]({link})'
            
            markdown_list += f'### {subreddit_name}\n\n'
            if description:
                markdown_list += f'{description}\n\n'
            markdown_list += f'{badge}\n\n'

    # Add instructions on how to update the list
    markdown_list += '\n## How to Update the List\n\n'
    markdown_list += '1. Edit the `subreddits.csv` file to add, remove, or modify subreddits.\n'
    markdown_list += '2. Run `python generate_readme.py` to regenerate the list.\n\n'

    # Read the existing README content
    with open(readme_file, 'r') as f:
        readme_content = f.read()

    # Find the Author section
    author_section = readme_content.find('## Author')
    if author_section == -1:
        print("Author section not found in README.md")
        return

    # Add the Author and Licensing sections
    markdown_list += readme_content[author_section:]

    # Write the updated content back to the README file
    with open(readme_file, 'w') as f:
        f.write(markdown_list)

if __name__ == "__main__":
    generate_readme('subreddits.csv', 'README.md')