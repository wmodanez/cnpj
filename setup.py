from setuptools import setup, find_packages
import os
import subprocess

# Ler README da API (para PyPI)
readme_path = os.path.join("cnpj_processor", "README.md")
with open(readme_path, "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Ler requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Obter versão do git tag ou arquivo VERSION
def get_version():
    """Obtém versão da tag git ou arquivo VERSION."""
    # Tentar ler arquivo VERSION (criado durante sdist)
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            return f.read().strip()
    
    # Tentar obter do git
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            # Remove 'v' prefix se existir
            version = version[1:] if version.startswith('v') else version
            
            # Salvar versão em arquivo para builds futuros
            with open(version_file, 'w') as f:
                f.write(version)
            
            return version
    except Exception as e:
        print(f"Erro ao obter versão do git: {e}")
    
    raise ValueError(
        "Não foi possível obter versão do git. "
        "Certifique-se de criar uma tag git antes de publicar: "
        "python scripts/release.py --major|--minor|--patch"
    )

version = get_version()

setup(
    name="cnpj-processor",
    version=version,
    author="Wesley Modanez Freitas",
    author_email="wesley.modanez@gmail.com",
    description="Sistema de Processamento de Dados CNPJ da Receita Federal do Brasil",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wmodanez/cnpj",
    project_urls={
        "Bug Tracker": "https://github.com/wmodanez/cnpj/issues",
        "Documentation": "https://github.com/wmodanez/cnpj/blob/develop/README.md",
        "Source Code": "https://github.com/wmodanez/cnpj",
    },
    packages=find_packages(include=[
        'cnpj_processor',
        'cnpj_processor.*',
        'src',
        'src.*',
    ]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cnpj-processor=cnpj_processor.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.json"],
    },
    zip_safe=False,
)
