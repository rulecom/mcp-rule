"""
Setup script for mcp-rule package.
"""

from setuptools import setup, find_packages

setup(
    name="mcp-rule",
    version="0.1.0",
    description="Model Context Protocol implementation for Rule.io API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MCP Rule Developer",
    author_email="user@example.com",
    url="https://github.com/yourusername/mcp-rule",
    packages=find_packages(),
    install_requires=[
        "mcp>=0.1.0",
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-rule=mcp_rule.entrypoint:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
