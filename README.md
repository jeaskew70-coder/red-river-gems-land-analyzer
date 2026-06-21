# Red River Gems Land Analyzer

A simple, self-contained Python CLI tool that generates helpful research reports for people looking at land and homestead properties in the Red River region (Texas, Oklahoma, Arkansas, and Louisiana).

The script asks a few basic questions about a property and produces a clean, well-organized report covering:

- Estimated total purchase costs (including rough closing cost estimates)
- Estimated annual property taxes using current regional effective rates
- Cost of living information (groceries, gas, utilities, rent)
- Cultural and lifestyle factors for the area (more county/location-specific details where reliable information exists)
- A "Regional Insights & Things to Consider" section with practical, buyer-focused advice on mineral rights, water realities, special tax valuations, homesteading factors, connectivity, and local realities
- A practical checklist of important due-diligence items for rural land in the region

All data is based on reasonable 2025-2026 public estimates. No internet connection or API keys are required.

## Requirements

- Python 3.8 or newer
- Works on Windows, macOS, and Linux

**Optional** (for PDF output only):
- `pip install fpdf2`

The core script runs with zero external dependencies.

## Quick Start

1. Save `red_river_gems_land_analyzer.py` in a folder.
2. Open a terminal / PowerShell / Command Prompt in that folder.
3. Run:

   **PowerShell / Command Prompt (Windows):**
   ```
   python red_river_gems_land_analyzer.py
   ```

   **macOS / Linux:**
   ```
   python3 red_river_gems_land_analyzer.py
   ```

4. Answer the prompts:
   - State (TX, OK, AR, or LA)
   - County or nearest city
   - Acreage
   - Asking price
   - Whether utilities are available
   - (Optional) Intended use and any notes

5. Review the nicely formatted report in your terminal.
6. Choose whether to save a `.txt` version, a PDF (if `fpdf2` is installed), or both.

The script will ask if you want to analyze another property so you can run multiple reports in one session.

## Example Filenames

Reports are saved in the current working directory with names like:
- `RedRiverGems_LandReport_Paris_TX_20260614.txt`
- `RedRiverGems_LandReport_Bowie_County_TX_20260614.pdf`

## Data Notes & Limitations (Important)

- Property tax estimates use average effective rates for the state. Actual taxes on raw land (especially land that qualifies for agricultural, timber, or wildlife valuation) are often significantly lower. Always verify with the county appraisal district.
- Closing cost estimates (~3%) are planning figures. Real costs vary by lender, title company, survey needs, and county.
- Cost-of-living numbers are regional averages for rural/small-town areas and will differ based on your lifestyle and exact location.
- The lifestyle/cultural sections include county or town-specific details (markets, fairs, colleges, hospitals, events) when strong public information is available for the entered location; otherwise they use improved regional descriptions. The "Regional Insights & Things to Consider" section highlights practical realities (mineral rights, water, valuation programs, etc.). Specific counties and towns still vary widely.
- Flood risk, mineral rights, easements, soil conditions, and utility extension costs are highly property-specific. The checklist highlights the most common gotchas in this region.
- This tool is for research and educational purposes only. It is not financial, legal, tax, or real estate advice.

Always do your own due diligence and consult local professionals (appraisal district, real estate attorney familiar with mineral estates, surveyor, county extension agent, etc.).

## Customizing the Script

All the key data lives near the top of `red_river_gems_land_analyzer.py` in clearly labeled constants:

- `TAX_RATES`
- `CLOSING_COST_PCT`
- `COL_DATA` (cost of living)
- `LIFESTYLE_BY_STATE`
- `REGIONAL_INSIGHTS_BASE`, `STATE_INSIGHTS`, and `LOCATION_INSIGHTS` (for the practical "Regional Insights & Things to Consider" section)
- Location-aware logic in `get_lifestyle_details()` for the Cultural & Lifestyle Factors section

You can update numbers or add more location-specific insights and details as better data becomes available. The code is heavily commented to make this easy.

## PDF Support

If you want the option to save reports as PDF:

```
pip install fpdf2
```

Run the script again and choose the PDF or "both" option when prompted. If `fpdf2` is not installed, the script will politely tell you how to add it and will still let you save the text version.

## Tips

- For the most useful reports, be as specific as you can with the "county or nearest city" field (e.g., "Lamar County", "Idabel", "Texoma area").
- Run the script once with a property you already know well to see how the numbers and suggestions feel.
- Save both the `.txt` and `.pdf` versions if you want to share the report with family or a realtor.

## License / Use

Free to use and modify for personal or research purposes. Feel free to adapt it for your own Red River Gems projects.

---

Made for people researching land and homestead life in the beautiful Red River region. Verify everything locally and enjoy the journey!