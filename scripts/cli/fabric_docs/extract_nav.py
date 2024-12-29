import yaml
from bs4 import BeautifulSoup


def pascal_to_kebab(pascal_str):
    # Handle empty string
    if not pascal_str:
        return pascal_str

    # Add hyphen before uppercase letters and convert to lowercase
    result = pascal_str[0].lower()
    for i in range(1, len(pascal_str)):
        # Add hyphen only if:
        # 1. Current char is uppercase AND
        # 2. Previous char is lowercase OR
        # 3. Next char is lowercase (if it exists)
        if pascal_str[i].isupper() and (pascal_str[i - 1].islower() or (i + 1 < len(pascal_str) and pascal_str[i + 1].islower())):
            result += f"-{pascal_str[i].lower()}"
        else:
            result += pascal_str[i].lower()

    return result.replace(" ", "")


def kebab_to_snake(kebab_str):
    return kebab_str.replace("-", "_")


def extract_tree_structure(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    def process_tree(ul_element, level=0):
        result = {}

        for li in ul_element.find_all("li", recursive=False):
            span = li.find("span", class_="tree-expander")
            a = li.find("a", class_="tree-item")

            # Handle items with children (has span with tree-expander)
            if span:
                node_text = span.get_text().strip()
                node_text_kebab_case = pascal_to_kebab(node_text)
                sub_ul = li.find("ul", class_="tree-group")

                if level == 0:
                    result[node_text_kebab_case] = {"commands": {}}
                    if sub_ul:
                        result[node_text_kebab_case]["commands"] = process_tree(sub_ul, level + 1)
                else:
                    result[node_text_kebab_case] = {"commands": {}}
                    if sub_ul:
                        result[node_text_kebab_case]["commands"] = process_tree(sub_ul, level + 1)

            # Handle leaf nodes (has direct link)
            elif a:
                leaf_text = a.get_text().strip()
                leaf_text_kebab = pascal_to_kebab(leaf_text)
                parent = li.find_parent("ul").find_parent("li")
                if parent:
                    parent_span = parent.find("span", class_="tree-expander")
                    if parent_span:
                        parent_text = parent_span.get_text().strip()
                        result[leaf_text_kebab] = {
                            "function": kebab_to_snake(f"{pascal_to_kebab(leaf_text)}_{pascal_to_kebab(parent_text)}"),
                            "args": [],
                        }
                else:
                    # Handle top-level leaf nodes
                    result[leaf_text] = {"function": leaf_text.replace(" ", "_").lower(), "args": []}

        return result

    root_ul = soup.find("ul", class_="tree")

    # Get all top-level items
    top_level_items = []
    for li in root_ul.find_all("li", recursive=False):
        span = li.find("span", class_="tree-expander")
        a = li.find("a", class_="tree-item")
        if span:
            top_level_items.append(span.get_text().strip().replace(" ", "_").lower())
        elif a:
            top_level_items.append(a.get_text().strip().replace(" ", "_").lower())

    tree_structure = {"commands": process_tree(root_ul)}

    # Ensure all top-level sections are included
    # for item in top_level_items:
    #     if item not in tree_structure['commands']:
    #         tree_structure['commands'][pascal_to_kebab(item)] = {'commands': {}}

    return tree_structure


from pathlib import Path

path = Path(__file__)
# Example usage:
with open(path.parent / "navbar.html", "r", encoding="utf-8") as file:
    html_content = file.read()

tree_structure = extract_tree_structure(html_content)

# Convert to YAML and print
yaml_output = yaml.dump(tree_structure, sort_keys=False, allow_unicode=True)
print(yaml_output)

# Optionally save to file
with open(path.parent / "tree_structure.yaml", "w", encoding="utf-8") as file:
    yaml.dump(tree_structure, file, sort_keys=False, allow_unicode=True)
