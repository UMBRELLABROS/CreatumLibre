import ast
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

REPO_PATH = Path("src/creatumlibre")


def walk_directory(base: Path, jinja_entries: list, indent: int = 0):
    for path in sorted(base.iterdir()):
        name = path.name

        # Skip __pycache__, hidden files, non-Python files, and __init__.py
        if (
            name.startswith(".")
            or name == "__pycache__"
            or (path.is_file() and not name.endswith(".py"))
            or name == "__init__.py"
        ):
            continue

        if path.is_dir():
            walk_directory(path, jinja_entries, indent + 1)
        else:
            if (data := extract_class_info(path)) is not None:
                class_name, doc_string, methods = data

                root = "https://umbrellabros.github.io/CreatumLibre/"
                relative = path.relative_to(REPO_PATH.parent)
                module_path = "/".join(relative.with_suffix("").parts)
                link = f"{root}{module_path}.html"

                dict_data = {
                    "class_name": class_name,
                    "doc_string": doc_string,
                    "module_path": str(path),
                    "link": link,
                    "methods": methods,
                }
                jinja_entries.append(dict_data)
        # https://umbrellabros.github.io/CreatumLibre/creatumlibre/graphics/boolean_operations/image_boolean.html#merge


def extract_class_info(py_file):
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
    except SyntaxError as e:
        print(f"Syntax error in {py_file}: {e}")
        return None

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node) or "[No docstring]"
            methods = [
                n.name
                for n in node.body
                if isinstance(n, ast.FunctionDef) and not n.name.startswith("__")
            ]
            return node.name, docstring, methods
    return None


entries = []
walk_directory(REPO_PATH, entries)


env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
template = env.get_template("index_template.html")
html_output = template.render(entries=entries)

Path("docs/index.html").write_text(html_output, encoding="utf-8")
