import logging
import sys
from pathlib import Path
from textwrap import fill
from typing import Any

import mkdocs_gen_files
from mkdocs_gen_files import Nav

sys.path.append(Path(__file__).parent.as_posix())

from parser import parse_parser  # noqa: E402

sys.path.append((Path(__file__).parents[1] / "src").as_posix())
from fractal_task_tools._cli import main_parser  # noqa: E402


def to_markdown(
    data: dict[str, Any],
    level: int,
    parent_cmd: str | None = None,
) -> str:
    """
    Given a `data` object with keys `name`, `description` and `usage`, produce
    a markdown string.
    """

    # Create MarkDown string for title
    name = data["name"]
    if parent_cmd:
        title_str = "#" * (level + 2) + f" {parent_cmd} {name}\n"
    else:
        title_str = "#" * (level + 1) + f" {name}\n"

    # Create MarkDown string for description
    description = data["description"]
    description_str = f"{description}\n"

    # Create MarkDown string for usage code block
    usage = data["bare_usage"].replace(Path(__file__).name, "fractal-manifest")
    while "  " in usage:
        usage = usage.replace("  ", " ")
    usage = fill(
        usage,
        width=80,
        initial_indent="",
        subsequent_indent=(" " * 8),
        break_on_hyphens=False,
    )
    usage_str = f"```\n{usage}\n```\n"

    # Create MarkDown string for action groups
    action_groups_strings = []
    if "action_groups" in data.keys():
        for group in data["action_groups"]:
            title = group["title"]
            if title == "Available commands":
                continue
            elif title in [
                "Named Arguments",
                "Positional Arguments",
            ]:
                options = group["options"]
                action_groups_strings.append("#" * (level + 3) + f" {title}\n")
                for opt in options:
                    opt_name = ",".join(opt["name"])
                    opt_help = opt["help"]
                    default = str(opt["default"])
                    if (default == "None") or ("==SUPPRESS==" in default):
                        default = ""
                    else:
                        default = f" *Default*: `{default}`."
                    action_groups_strings.append(
                        f"- **`{opt_name}`**: {opt_help}{default}\n"
                    )
            else:
                raise NotImplementedError(title)

    action_groups_str = "\n".join(action_groups_strings)

    # Combine strings together
    md_string = (
        "\n".join(
            (
                title_str,
                description_str,
                usage_str,
                action_groups_str,
            )
        )
        + "\n"
    )

    return md_string


nav = Nav()

# Parser level 0
for key in ["fractal_task_tools", "fractal-manifest"]:
    nav[[key]] = f"{key}/index.md"

# API
logger = logging.getLogger(f"mkdocs.plugins.{__name__}")
prefix = f"[{Path(__file__).name}]"
logger.info(f"{prefix} START")
for path in sorted(Path("src/fractal_task_tools").rglob("*.py")):
    rel_doc_path = path.relative_to("src").with_suffix(".md")
    full_doc_path = Path(
        "reference",
        rel_doc_path,
    )
    parts = list(rel_doc_path.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
        rel_doc_path = rel_doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = rel_doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        fd.write(f"::: {identifier}")

    # mkdocs_gen_files.set_edit_path(full_doc_path, path)

logger.info(f"{prefix} END")

# CLI
main = parse_parser(main_parser)
main["name"] = "fractal-manifest"
with mkdocs_gen_files.open("reference/fractal-manifest/index.md", "w") as f:
    f.write(to_markdown(main, level=0))
for child in main["children"]:
    name = child["name"]
    nav[["fractal-manifest", name]] = f"fractal-manifest/{name}/index.md"
    with mkdocs_gen_files.open(f"reference/fractal-manifest/{name}/index.md", "w") as f:
        f.write(to_markdown(child, level=0))


summary_path = "reference/SUMMARY.md"
logger.info(f"{prefix} {summary_path=}")
with mkdocs_gen_files.open(summary_path, "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
