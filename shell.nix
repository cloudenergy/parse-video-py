{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    aiofiles
    annotated-types
    anyio
    black
    beautifulsoup4
    certifi
    cfgv
    click
    colorama
    cssselect
    distlib
    exceptiongroup
    fake-useragent
    faker
    fastapi
    filelock
    flake8
    h11
    httpcore
    httptools
    httpx
    identify
    idna
    isort
    jinja2
    jmespath
    lxml # System dependencies added in buildInputs
    markdown-it-py
    markupsafe
    mccabe
    mdurl
    mypy-extensions
    nodeenv
    packaging
    parsel
    pathspec
    platformdirs
    pycodestyle
    pydantic
    pyflakes
    pygments
    python-dateutil
    python-dotenv
    pyyaml
    rich
    shellingham
    six
    sniffio
    starlette
    tomli
    typer # Includes typer-cli
    typing-extensions
    uvicorn
    w3lib
    watchfiles
    websockets
  ]);
in
pkgs.mkShell {
  name = "parse-video-py-env";

  # Packages available in the shell
  buildInputs = [
    # The Python environment with specified packages
    pythonEnv

    # System libraries needed by lxml
    pkgs.libxml2
    pkgs.libxslt
    pkgs.zlib # Often a dependency for libxml2/libxslt

    # Python dev tools are now part of pythonEnv
    pkgs.pre-commit

    # Add other system dependencies if required by any parser
    # pkgs.git # Example: if pre-commit needs it
  ];

  # Optional: Commands to run when entering the shell
  # shellHook = ''
  #   echo "Entered Python development environment for parse-video-py"
  #   # Example: Set PYTHONPATH if needed, though often not required with withPackages
  #   # export PYTHONPATH="${pkgs.lib.makeSearchPath "lib/python${pythonEnv.pythonVersion}/site-packages" [ pythonEnv ]}:${PYTHONPATH:-}"
  # '';
} 