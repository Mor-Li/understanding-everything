"""
测试脚本：单独生成一个 README.md 文件
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path to import from scripts
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.s2_generate_readme import (
    collect_folder_content,
    generate_tree_structure,
    ask_gemini_async,
)
from openai import AsyncOpenAI


async def main():
    # 从命令行参数获取配置，或使用默认值
    if len(sys.argv) > 1:
        explain_base = Path(sys.argv[1])
    else:
        explain_base = Path("output/SELF-PARAM/explain-2025-05-18")

    folder_path = Path(".")  # 根目录

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    if not api_key:
        print("❌ 需要设置环境变量 OPENAI_API_KEY")
        return

    print(f"📂 目标文件: {explain_base / 'README.md'}")
    print()

    # 1. 生成目录树结构
    print("🌲 生成目录树结构...")
    tree_structure = generate_tree_structure(folder_path, explain_base)
    print(f"目录树:\n{tree_structure}")
    print()

    # 2. 收集文件夹内容
    print("📄 收集文件夹内容...")
    content = collect_folder_content(folder_path, explain_base)
    print(f"内容长度: {len(content)} 字符")
    print()

    # 3. 调用 API 生成 README
    print("🤖 调用 Gemini API 生成 README...")
    client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    folder_display_name = explain_base.parent.name  # "SELF-PARAM"

    readme_content = await ask_gemini_async(
        folder_display_name,
        content,
        tree_structure,
        client,
        "gemini-3-pro-preview"
    )

    # 4. 保存结果
    readme_path = explain_base / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {folder_display_name}\n\n")
        f.write(readme_content)

    print(f"✅ 成功生成 README: {readme_path}")
    print()
    print("=" * 60)
    print("生成的 README 内容预览（前 500 字符）:")
    print("=" * 60)
    print(readme_content[:500])
    print("...")


if __name__ == "__main__":
    asyncio.run(main())
