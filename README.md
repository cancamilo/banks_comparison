# Mortgage Tools

A collection of tools for mortgage calculations and bank offer comparisons.

## Features

### 1. Mortgage Calculator (`mortgage_calculator.ipynb`)
- Calculate monthly payments for French-style (annuity) mortgages
- Generate complete amortization schedules
- View principal, interest, and remaining balance for each payment

### 2. Bank Comparison Tool (`bank_comparison.ipynb`)
- Compare multiple bank mortgage offers
- Calculate ROCE (Return on Capital Employed) for each option
- Identify the best mortgage option based on ROCE

### 3. Streamlit Web App (`app.py`)
- **Mobile-friendly web application** for comparing bank offers on the go
- Add multiple bank offers dynamically
- Real-time ROCE calculations
- Accessible from your phone browser

## Quick Start

### Run the Streamlit App Locally

```bash
# Option 1: Use the script
./run_app.sh

# Option 2: Direct command
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Access from Your Phone (Local Network)

1. Make sure your phone and computer are on the same Wi-Fi network
2. Find your computer's IP address:
   - **Mac/Linux:** `ifconfig | grep "inet "`
   - **Windows:** `ipconfig`
3. On your phone, go to: `http://YOUR_IP:8501`

## Deploy to Streamlit Cloud (Recommended)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Quick steps:**
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!
5. Add the URL to your phone's home screen

## ROCE Calculation

**ROCE = (Annual Rental Income - Annual Mortgage Costs - Annual Fees) / Down Payment × 100**

This metric helps you identify which mortgage offer provides the best return on your invested capital.

## Requirements

All dependencies are managed via `pyproject.toml`:
- `pandas` - Data manipulation
- `numpy` - Numerical calculations
- `jupyter` - Notebook support
- `streamlit` - Web app framework

Install with:
```bash
uv sync
```

## Project Structure

```
mortgage-tools/
├── app.py                      # Streamlit web app
├── mortgage_calculator.ipynb   # Single mortgage calculator
├── bank_comparison.ipynb       # Bank comparison notebook
├── run_app.sh                  # Quick start script
├── DEPLOYMENT.md               # Deployment instructions
└── pyproject.toml              # Dependencies
```

## Usage Examples

### Notebook Usage

1. Open `mortgage_calculator.ipynb` for single mortgage calculations
2. Open `bank_comparison.ipynb` to compare multiple banks
3. Modify input parameters and run cells

### Web App Usage

1. Run `streamlit run app.py`
2. Enter property details in the sidebar
3. Add bank offers using the form
4. Click "Calculate Comparison" to see results
5. The best option (highest ROCE) is highlighted automatically

## License

MIT

