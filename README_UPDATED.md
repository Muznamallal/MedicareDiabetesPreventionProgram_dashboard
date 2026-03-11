# Medicare Diabetes Prevention Program (MDPP) Dashboard 🩺

A **Streamlit-powered interactive dashboard** to explore CMS Medicare Diabetes Prevention Program (MDPP) supplier data and its impact on preventive care for Medicare beneficiaries with prediabetes.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📊 Features

- **Interactive KPIs**: View total suppliers, states covered, and location breakdowns
- **Geographic Filtering**: Filter by state and location type (Administrative vs Community Setting)
- **Interactive Map**: Visualize MDPP supplier locations across the United States
- **Data Explorer**: Search and filter supplier data with an interactive table
- **Preventive Care Insights**: Understand how MDPP supports diabetes prevention
- **Medicare Advantage Analytics**: Explore CMS Program Statistics for MA beneficiaries
- **Provider Search**: Search Medicare-enrolled physicians, practitioners, and suppliers

## 🎯 What is MDPP?

The **Medicare Diabetes Prevention Program (MDPP)** is a CDC-recognized lifestyle change program for Medicare beneficiaries with prediabetes. The program helps participants:

- Lower their risk of developing type 2 diabetes
- Adopt healthier eating habits
- Increase physical activity
- Make sustainable behavior changes

This dashboard helps identify where MDPP services are available and reveals gaps in coverage.

## 📸 Screenshots

*Add your dashboard screenshots here after running the app*

### Dashboard Overview
![Dashboard Overview](screenshots/overview.png)

### Interactive Map
![MDPP Supplier Map](screenshots/map.png)

### Data Explorer
![Data Table](screenshots/data-table.png)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Muznamallal/MedicareDiabetesPreventionProgram_dashboard.git
   cd MedicareDiabetesPreventionProgram_dashboard
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Mac/Linux
   # OR
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add the data files**
   
   The app will automatically look for the MDPP CSV in these locations:
   - `Medicare Diabetes Prevention Program/2026-Q1/MDPP_Supplier_Mapping_02.01.26.csv`
   - `data/MDPP_Supplier_Mapping_02.01.26.csv`
   
   Place your CSV file in one of these locations, or the app will search for any MDPP CSV in the `data/` folder.

5. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   
   The dashboard will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
MedicareDiabetesPreventionProgram_dashboard/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/                          # Data files directory (optional)
│   └── MDPP_Supplier_Mapping_02_01_26.csv
├── Medicare Diabetes Prevention Program/  # Alternative data location
│   └── 2026-Q1/
│       └── MDPP_Supplier_Mapping_02.01.26.csv
└── screenshots/                   # Dashboard screenshots (add these)
    ├── overview.png
    ├── map.png
    └── data-table.png
```

## 📊 Data Sources

### Primary Data
- **CMS Medicare Diabetes Prevention Program (MDPP) Supplier Mapping**
  - Organization names, locations, NPIs
  - State and category information
  - Geographic coordinates
  - Updated quarterly by CMS

### Additional Data (Optional)
- **CMS Program Statistics - Medicare Advantage**: Physician and supplier utilization data
- **CMS Provider Data API**: Real-time Medicare provider enrollment data

## 🎨 Dashboard Tabs

1. **Overview**: Key metrics and summary statistics
2. **Map**: Interactive geographic visualization of suppliers
3. **Data**: Searchable and filterable supplier table
4. **Preventive Care**: Information about MDPP's role in diabetes prevention
5. **Medicare Advantage**: CMS Program Statistics analysis
6. **Provider Search**: Medicare provider lookup tool

## 🔧 Configuration

The app automatically searches for data files in predefined locations. To customize data paths, modify the `find_mdpp_csv()` function in `app.py`.

## 📈 Use Cases

- **Policymakers**: Identify coverage gaps and target expansion areas
- **Care Coordinators**: Connect beneficiaries with local MDPP services
- **Researchers**: Analyze MDPP supplier distribution patterns
- **Healthcare Organizations**: Assess preventive care accessibility

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Data provided by the Centers for Medicare & Medicaid Services (CMS)
- Built with [Streamlit](https://streamlit.io/)
- Inspired by the need to improve preventive care access

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Last Updated**: March 2026 | **Data Version**: Q1 2026
