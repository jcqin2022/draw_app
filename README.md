# draw_app

## descripton
small draw app.

## build
1. Create a virtual environment
    ```
    python -m venv .venv 
    ```
2. Activate your environment
    ```
    .\.venv\Scripts\activate
    ```
3. Install package management tool
    ```
    pip install pdm
    ```
4. Install dependencies
    ```
    pdm install
    ```
## dist
1. Install installer tool
    ```
    pdm add pyinstaller
    ```
2. Generate dist
    ```
    pyinstaller whiteboard.spec
    ```