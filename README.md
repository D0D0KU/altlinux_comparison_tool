# Package Comparison Tool

This Python script compares binary packages between two branches of the Alt Linux distribution.

## Usage

1. Clone the repository:
```bash
git clone https://github.com/D0D0KU/altlinux_comparison_tool.git
```
2. Navigate to the project directory:
```bash
cd your-repository
```
3. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
```
4. Activate the virtual environment:
```bash
source venv/bin/activate
```
5. Install the required dependencies:
```bash
pip install -r requirements.txt
```
6. Run the script:
If you want to output data to the terminal:
```bash
python package_comparison.py sisyphus p10
```
If you want to save the result to json, pass the optional argument --output-file fale_name:
```bash
python package_comparison.py sisyphus p10 --output-file result.json
```
