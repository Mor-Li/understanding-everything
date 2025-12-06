"""
utils.py
通用工具函数
"""

from datetime import datetime
from pathlib import Path

import git


def get_commit_date(repo_path: str) -> str:
    """
    获取仓库最新 commit 的日期

    Args:
        repo_path: 仓库路径

    Returns:
        日期字符串 (YYYY-MM-DD 格式)

    Raises:
        Exception: 如果无法获取 commit 日期
    """
    try:
        repo = git.Repo(repo_path)
        latest_commit = repo.head.commit
        commit_date = datetime.fromtimestamp(latest_commit.committed_date)
        return commit_date.strftime("%Y-%m-%d")
    except Exception as e:
        raise Exception(f"无法获取 {repo_path} 的 commit 日期: {e}")


def get_output_path(repo_path: str, subdir: str, output_type: str) -> str:
    """
    根据 git commit 日期生成带时间戳的 output 路径

    Args:
        repo_path: 仓库路径
        subdir: 子目录名称
        output_type: 输出类型 (explain, website, heatmap 等)

    Returns:
        带时间戳的 output 路径字符串
        例如: "output/Megatron-LM/explain-2025-03-20"
    """
    repo_name = Path(repo_path).name
    commit_date = get_commit_date(repo_path)

    return f"output/{repo_name}/{output_type}-{commit_date}"


def get_output_base(repo_path: str) -> str:
    """
    获取 output 基础路径（不含时间戳）

    Args:
        repo_path: 仓库路径

    Returns:
        output 基础路径字符串
        例如: "output/Megatron-LM"
    """
    repo_name = Path(repo_path).name
    return f"output/{repo_name}"
