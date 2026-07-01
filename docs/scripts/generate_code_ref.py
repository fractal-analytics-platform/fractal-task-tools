from pathlib import Path


def get_subpackages(base_path: Path) -> list[Path]:
    subpkgs = list(
        subpkg_dir
        for subpkg_dir in base_path.glob("*")
        if (subpkg_dir.is_dir() and (subpkg_dir / "__init__.py").exists())
    )
    subpkgs = sorted(subpkgs)
    return subpkgs


def _sort_key(path: Path) -> int:
    """
    List private modules first.
    """
    return 0 if path.name.startswith("_") else 1


def get_modules(base_path: Path) -> list[Path]:
    modules = list(m for m in base_path.glob("*.py") if m.name != "__init__.py")
    modules = sorted(modules, key=_sort_key)
    return modules


PKG_NAME = "fractal_task_tools"
BASE_CODE_DIR = Path("src/fractal_task_tools")
BASE_DOCS_DIR = Path("docs/code_reference")
BASE_DOCS_DIR.mkdir(exist_ok=True, parents=True)


def walk_and_build(base_path: Path):
    print(f"[WALK {base_path}] START")
    relative_path = base_path.relative_to(BASE_CODE_DIR)
    relative_string_dots = relative_path.as_posix().replace("/", ".").strip(".")
    title = f"{PKG_NAME}.{relative_string_dots}".strip(".")
    index_path = BASE_DOCS_DIR / base_path.relative_to(BASE_CODE_DIR) / "index.md"
    with index_path.open("w") as f:
        f.write(f"# `{title}`\n\n")
        ref = f"{PKG_NAME}.{relative_string_dots}".strip(".")
        f.write(f"::: {ref}\n")

        print(f"[WALK {base_path}] SUBPACKAGES")
        subpkgs = get_subpackages(base_path)
        if subpkgs:
            f.write("## Subpackages\n\n")
            for subpkg in subpkgs:
                relative_subpkg_path = subpkg.relative_to(BASE_CODE_DIR)
                docs_subpkg_path = BASE_DOCS_DIR / relative_subpkg_path
                docs_subpkg_path.mkdir(parents=True, exist_ok=True)
                f.write(
                    f"- [{relative_subpkg_path.as_posix()}](./{relative_subpkg_path})\n"
                )
                walk_and_build(subpkg)
            f.write("\n")

        print(f"[WALK {base_path}] MODULES")
        modules = get_modules(base_path)
        if modules:
            # f.write("## Modules\n\n")
            for module in modules:
                relative_module_path = module.relative_to(BASE_CODE_DIR).with_suffix("")
                relative_module_string = relative_module_path.as_posix()
                relative_module_string_dots = relative_module_string.replace("/", ".")
                docs_path = BASE_DOCS_DIR / relative_module_path.with_suffix(".md")
                # f.write(f"- [{relative_module_string}](./{docs_path.name})\n")
                with docs_path.open("w") as f1:
                    f1.write(f"::: {PKG_NAME}.{relative_module_string_dots}\n")
                print(f"[WALK {base_path}] {relative_module_path}, {docs_path}")
            f.write("\n")
    print(f"END WALK {base_path}")


if __name__ == "__main__":
    walk_and_build(BASE_CODE_DIR)
