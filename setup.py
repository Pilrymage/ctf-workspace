from __future__ import annotations

import argparse
import csv
import re
import shutil
from pathlib import Path


INVALID_CHARS = '<>:"/\\|?*'
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def sanitize_component(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("目录名不能为空")

    cleaned = re.sub(f"[{re.escape(INVALID_CHARS)}]", "_", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")

    if not cleaned:
        raise ValueError(f"无法从 {value!r} 生成合法目录名")

    if cleaned.upper() in WINDOWS_RESERVED_NAMES:
        cleaned = f"{cleaned}_"

    return cleaned


def copy_template_tree(template_dir: Path, target_dir: Path, overwrite: bool) -> None:
    for source in template_dir.rglob("*"):
        relative_path = source.relative_to(template_dir)
        destination = target_dir / relative_path

        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        if overwrite or not destination.exists():
            shutil.copy2(source, destination)


def iter_challenges(csv_path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.reader(csv_file, skipinitialspace=True)
        for index, row in enumerate(reader, start=1):
            if not row or not any(cell.strip() for cell in row):
                continue

            if len(row) < 2:
                raise ValueError(f"CSV 第 {index} 行少于两列: {row!r}")

            category = row[0].strip()
            challenge = row[1].strip()
            if not category or not challenge:
                raise ValueError(f"CSV 第 {index} 行存在空字段: {row!r}")

            records.append((category, challenge))

    return records


def generate_structure(root_dir: Path, csv_path: Path, template_dir: Path, overwrite: bool) -> None:
    if not csv_path.is_file():
        raise FileNotFoundError(f"找不到 CSV 文件: {csv_path}")

    if not template_dir.is_dir():
        raise FileNotFoundError(f"找不到模板目录: {template_dir}")

    records = iter_challenges(csv_path)
    if not records:
        raise ValueError("CSV 文件为空，没有可生成的目录")

    seen_paths: dict[Path, tuple[str, str]] = {}

    for raw_category, raw_challenge in records:
        category = sanitize_component(raw_category)
        challenge = sanitize_component(raw_challenge)
        target_dir = root_dir / category / challenge

        previous = seen_paths.get(target_dir)
        if previous and previous != (raw_category, raw_challenge):
            raise ValueError(
                "清理后的目录名发生冲突: "
                f"{previous!r} 与 {(raw_category, raw_challenge)!r} 都映射到 {target_dir}"
            )

        seen_paths[target_dir] = (raw_category, raw_challenge)
        target_dir.mkdir(parents=True, exist_ok=True)
        copy_template_tree(template_dir, target_dir, overwrite=overwrite)
        print(f"已生成: {target_dir.relative_to(root_dir)}")


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(
        description="根据 challenges.csv 生成两级题目目录，并填充 .template 文件"
    )
    parser.add_argument(
        "--csv",
        default=base_dir / "challenges.csv",
        type=Path,
        help="CSV 文件路径，默认使用当前目录下的 challenges.csv",
    )
    parser.add_argument(
        "--template",
        default=base_dir / ".template",
        type=Path,
        help="模板目录路径，默认使用当前目录下的 .template",
    )
    parser.add_argument(
        "--root",
        default=base_dir,
        type=Path,
        help="输出根目录，默认使用脚本所在目录",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="覆盖已存在的模板文件，默认仅复制缺失文件",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generate_structure(
        root_dir=args.root.resolve(),
        csv_path=args.csv.resolve(),
        template_dir=args.template.resolve(),
        overwrite=args.overwrite,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
