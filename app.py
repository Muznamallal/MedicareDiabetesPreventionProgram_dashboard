"""
CMS Medicare Diabetes Preventive Program (MDPP) Dashboard
Streamlit app for exploring MDPP supplier data and preventive care impact.
"""

import os
import re
import streamlit as st
import pandas as pd
import requests

# Page config
st.set_page_config(
    page_title="MDPP Dashboard | Medicare Diabetes Prevention",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .main-header { font-size: 2rem; font-weight: 700; color: #1e3a5f; margin-bottom: 0.5rem; }
    .sub-header { color: #5a6c7d; margin-bottom: 1.5rem; }
    .metric-card { background: linear-gradient(135deg, #f0f7ff 0%, #e8f4fc 100%); padding: 1rem 1.25rem; border-radius: 10px; border-left: 4px solid #1e88e5; margin: 0.5rem 0; }
    .preventive-box { background: #f1f8e9; padding: 1rem 1.25rem; border-radius: 10px; border-left: 4px solid #7cb342; margin: 0.5rem 0; }
    .stDataFrame { font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)


def find_mdpp_csv():
    """Locate MDPP CSV in project (extracted from zip or in data folder)."""
    base = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base, "Medicare Diabetes Prevention Program", "2026-Q1", "MDPP_Supplier_Mapping_02.01.26.csv"),
        os.path.join(base, "data", "MDPP_Supplier_Mapping_02.01.26.csv"),
        os.path.join(base, "data", "MDPP_Supplier_Mapping_01.01.26.csv"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    # Fallback: any CSV in data/ or in extracted folder
    for folder in ["Medicare Diabetes Prevention Program/2026-Q1", "Medicare Diabetes Prevention Program", "data"]:
        folder_path = os.path.join(base, folder)
        if os.path.isdir(folder_path):
            for f in os.listdir(folder_path):
                if f.endswith(".csv") and "MDPP" in f.upper():
                    return os.path.join(folder_path, f)
    return None


def find_cps_ma_excel():
    """Locate CMS Program Statistics Medicare Advantage Excel file."""
    base = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base, "data", "cps_physsupp_ma_2016", "CPS MDCR PHYSSUPP MA 2016 FINAL.xlsx"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    # Fallback: search data/ for a matching Excel file
    data_dir = os.path.join(base, "data")
    if os.path.isdir(data_dir):
        for root, _dirs, files in os.walk(data_dir):
            for f in files:
                name_upper = f.upper()
                if f.lower().endswith((".xlsx", ".xls")) and "PHYSSUPP" in name_upper and "MA" in name_upper:
                    return os.path.join(root, f)
    return None


def parse_lat_lon(location_str):
    """Extract (lat, lon) from Location 1 string like '... (48.231903, -101.28614)'."""
    if pd.isna(location_str) or not isinstance(location_str, str):
        return None, None
    match = re.search(r"\((-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)", location_str)
    if match:
        try:
            return float(match.group(1)), float(match.group(2))
        except ValueError:
            pass
    return None, None


@st.cache_data
def load_mdpp_data(csv_path):
    """Load and preprocess MDPP supplier CSV."""
    df = pd.read_csv(csv_path)
    # Normalize column names (strip spaces)
    df.columns = df.columns.str.strip()
    # Parse coordinates from Location 1 if present
    if "Location 1" in df.columns:
        coords = df["Location 1"].apply(parse_lat_lon)
        df["lat"] = [c[0] for c in coords]
        df["lon"] = [c[1] for c in coords]
    return df


@st.cache_data
def load_cps_ma_data(xlsx_path):
    """Load CMS Program Statistics – Medicare Advantage physician/supplier Excel.

    Returns:
        dict: {sheet_name: DataFrame}
    """
    try:
        xls = pd.ExcelFile(xlsx_path)
    except Exception as exc:
        st.warning(f"Could not read CPS MA workbook: {exc}")
        return {}
    data: dict[str, pd.DataFrame] = {}

    for sheet in xls.sheet_names:
        try:
            if sheet == "MDCR PHYSSUPP MA 2":
                # Demographics / age table
                df = xls.parse(sheet, skiprows=5)
                df.columns = [
                    "Age group",
                    "Medicare beneficiaries",
                    "Persons with utilization",
                    "Total services",
                    "Percent of total services",
                    "Services per person",
                    "Services per person with utilization",
                ][: len(df.columns)]
                data[sheet] = df
            elif sheet == "MDCR PHYSSUPP MA 3":
                # Area of residence (states, regions)
                df = xls.parse(sheet, skiprows=5)
                df.columns = [
                    "Area",
                    "Medicare beneficiaries",
                    "Persons with utilization",
                    "Total services",
                    "Services per person",
                    "Services per person with utilization",
                ][: len(df.columns)]
                data[sheet] = df
            elif sheet == "MDCR PHYSSUPP MA 5":
                # Service types (BETOS / RBCS categories)
                df = xls.parse(sheet, skiprows=5)
                df.columns = [
                    "Service category",
                    "Persons with utilization",
                    "Total services",
                    "Services per person",
                    "Services per person with utilization",
                ][: len(df.columns)]
                data[sheet] = df
            else:
                data[sheet] = xls.parse(sheet)
        except Exception:
            continue

    return data


CMS_PROVIDER_API = "https://data.cms.gov/data-api/v1/dataset/2457ea29-fc82-48b0-86ec-3b0755de7515/data"


@st.cache_data(ttl=3600)
def fetch_provider_data(limit: int = 5000):
    """Fetch Medicare provider data from CMS API."""
    try:
        resp = requests.get(CMS_PROVIDER_API, params={"size": limit}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.warning(f"Could not fetch provider data: {e}")
        return []


def main():
    csv_path = find_mdpp_csv()
    if not csv_path:
        st.error(
            "**MDPP data not found.** Please ensure the CSV is either:\n"
            "- Extracted from your zip into: `Medicare Diabetes Prevention Program/2026-Q1/MDPP_Supplier_Mapping_02.01.26.csv`\n"
            "- Or placed in a `data/` folder as `MDPP_Supplier_Mapping_*.csv`"
        )
        return

    df = load_mdpp_data(csv_path)

    # Header
    st.markdown('<p class="main-header">🩺 Medicare Diabetes Preventive Program (MDPP) Dashboard</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">CMS supplier locations and how MDPP supports preventive care for Medicare beneficiaries with prediabetes.</p>',
        unsafe_allow_html=True,
    )

    # Sidebar filters
    st.sidebar.header("Filters")
    states = ["All"] + sorted(df["State"].dropna().astype(str).unique().tolist())
    selected_state = st.sidebar.selectbox("State", states)
    categories = ["All"] + (df["Category"].dropna().astype(str).unique().tolist() if "Category" in df.columns else [])
    selected_category = st.sidebar.selectbox("Category", categories)

    # Apply filters
    mask = pd.Series(True, index=df.index)
    if selected_state != "All":
        mask &= df["State"].astype(str) == selected_state
    if selected_category != "All" and "Category" in df.columns:
        mask &= df["Category"].astype(str) == selected_category
    filtered = df[mask]

    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total locations", f"{len(filtered):,}")
    with col2:
        n_orgs = filtered["Organization Name"].nunique() if "Organization Name" in filtered.columns else 0
        st.metric("Unique organizations", f"{n_orgs:,}")
    with col3:
        n_states = filtered["State"].nunique() if "State" in filtered.columns else 0
        st.metric("States covered", f"{n_states:,}")
    with col4:
        n_community = (filtered["Category"] == "Community Setting").sum() if "Category" in filtered.columns else 0
        st.metric("Community settings", f"{n_community:,}")

    # Tabs
    tab_overview, tab_map, tab_table, tab_preventive, tab_ma, tab_provider = st.tabs(
        ["Overview", "Map", "Data table", "Preventive care", "MA utilization", "Provider Search"]
    )

    with tab_overview:
        st.subheader("By state")
        if "State" in filtered.columns:
            state_counts = filtered["State"].value_counts().sort_values(ascending=True)
            st.bar_chart(state_counts)
        st.subheader("By category")
        if "Category" in filtered.columns:
            cat_counts = filtered["Category"].value_counts()
            st.bar_chart(cat_counts)

    with tab_map:
        map_df = filtered.copy()
        if "lat" in map_df.columns and "lon" in map_df.columns:
            map_df = map_df.dropna(subset=["lat", "lon"])
        if len(map_df) > 0 and "lat" in map_df.columns:
            st.map(map_df[["lat", "lon"]].rename(columns={"lat": "lat", "lon": "lon"}), use_container_width=True)
        else:
            st.info("No coordinates available for mapping. Location 1 column may use a different format.")

    with tab_table:
        display_cols = [c for c in ["Organization Name", "Location Name", "City", "State", "ZIP Code", "Telephone Number", "Category"] if c in filtered.columns]
        if display_cols:
            st.dataframe(filtered[display_cols], use_container_width=True, height=400)
        else:
            st.dataframe(filtered, use_container_width=True, height=400)

    with tab_preventive:
        st.markdown(
            """
            ### How MDPP supports preventive care

            The **Medicare Diabetes Prevention Program (MDPP)** is a CDC-recognized lifestyle change program for people with Medicare who have prediabetes. This dashboard helps you see **where** those services are available.

            - **Find a supplier:** Use the **Map** and **Data table** tabs to find MDPP suppliers by state and location type (Administrative vs Community Setting).
            - **Prevent progression:** MDPP helps eligible beneficiaries lower their risk of developing type 2 diabetes through structured coaching on diet, physical activity, and behavior change.
            - **Use the data:** Policymakers and care coordinators can use this data to identify gaps in coverage (states or regions with few suppliers) and target outreach for preventive care.
            """
        )
        st.markdown('<p class="preventive-box"><strong>Data source:</strong> CMS Medicare Diabetes Prevention Program – supplier mapping (public). Updated quarterly. Use it to connect beneficiaries to local MDPP services for preventive care.</p>', unsafe_allow_html=True)

    with tab_ma:
        st.subheader("CMS Program Statistics – Medicare Advantage (physicians, practitioners, suppliers)")
        cps_path = find_cps_ma_excel()
        if not cps_path:
            st.info(
                "CMS Program Statistics Excel file not found.\n\n"
                "Expected path (already downloaded earlier): "
                "`data/cps_physsupp_ma_2016/CPS MDCR PHYSSUPP MA 2016 FINAL.xlsx`.\n"
                "If you move or replace the file, update the path in the app."
            )
        else:
            cps_data = load_cps_ma_data(cps_path)
            if not cps_data:
                st.info("Workbook was found but no readable sheets were detected.")
            else:
                sheet_names = list(cps_data.keys())

                def find_sheet(tag: str):
                    tag_upper = tag.upper()
                    for name in sheet_names:
                        name_upper = str(name).upper()
                        if "MDCR" in name_upper and "PHYSSUPP" in name_upper and tag_upper in name_upper:
                            return name
                    return None

                sheet_ma2 = find_sheet("MA 2")
                sheet_ma3 = find_sheet("MA 3")
                sheet_ma5 = find_sheet("MA 5")

                st.markdown(
                    "These CMS Program Statistics tables summarize **utilization for Medicare Advantage beneficiaries** "
                    "by demographics, geography, and service type. Below are focused views from key tables."
                )

                # MA 2 – demographics and age
                if sheet_ma2 is not None:
                    st.markdown("### MDCR PHYSSUPP MA 2 – by demographics and age")
                    df2 = cps_data[sheet_ma2].copy()
                    # Clean age groups and keep meaningful rows
                    if "Age group" in df2.columns:
                        df2 = df2[df2["Age group"].notna()]
                        df2 = df2[~df2["Age group"].astype(str).str.upper().str.contains("BLANK")]
                        df2 = df2[df2["Age group"].astype(str).str.strip() != ""]
                        if "Total services" in df2.columns:
                            st.markdown("#### Total services by age group")
                            age_services = (
                                df2.set_index("Age group")["Total services"]
                                .dropna()
                            )
                            st.bar_chart(age_services)

                # MA 3 – by area of residence (state / region)
                if sheet_ma3 is not None:
                    st.markdown("### MDCR PHYSSUPP MA 3 – by area of residence")
                    df3 = cps_data[sheet_ma3].copy()
                    if "Area" in df3.columns and "Total services" in df3.columns:
                        df3 = df3[df3["Area"].notna()]
                        df3 = df3[~df3["Area"].astype(str).str.upper().str.contains("BLANK")]
                        df3 = df3[df3["Area"].astype(str).str.strip() != ""]
                        # Exclude national totals (United States, All Areas, etc.)
                        exclude = {"UNITED STATES", "ALL AREAS"}
                        df3 = df3[~df3["Area"].astype(str).str.upper().str.strip().isin(exclude)]
                        st.markdown("#### Total services by area of residence")
                        area_services = (
                            df3.set_index("Area")["Total services"]
                            .dropna()
                        )
                        st.bar_chart(area_services)

                # MA 5 – service mix / BETOS
                if sheet_ma5 is not None:
                    st.markdown("### MDCR PHYSSUPP MA 5 – by service type (BETOS / category)")
                    df5 = cps_data[sheet_ma5].copy()
                    if "Service category" in df5.columns and "Total services" in df5.columns:
                        df5 = df5[df5["Service category"].notna()]
                        df5 = df5[df5["Service category"].astype(str).str.strip() != ""]
                        st.markdown("#### Service mix by category")
                        service_summary_5 = (
                            df5.set_index("Service category")["Total services"]
                            .dropna()
                            .sort_values(ascending=False)
                            .head(20)
                        )
                        st.bar_chart(service_summary_5)

                        st.markdown(
                            """
                            These categories show **what kinds of services**
                            Medicare Advantage beneficiaries are using most (for example, office visits,
                            imaging, procedures). Combined with MDPP locations, this helps you see where
                            high-use service areas might benefit from **more preventive diabetes programs**.
                            """
                        )

                st.markdown(
                    """
                    **How this relates to preventive care**

                    - MDPP locations (other tabs) show **where lifestyle change programs are offered** for beneficiaries with prediabetes.
                    - CMS Program Statistics tables here show **how beneficiaries are actually using physician and supplier services** in Medicare Advantage.
                    - Together, you can:
                      - Compare **where MDPP access exists** vs. **where service utilization is high or low**.
                      - Identify states or regions where you might want to **expand preventive services** or **target outreach**.
                    """
                )

    with tab_provider:
        st.subheader("Medicare Provider Search")
        st.markdown(
            "Search physicians, non-physician practitioners, and suppliers enrolled in Medicare. "
            "Data from [CMS Provider Data](https://data.cms.gov/data-api/v1/dataset/2457ea29-fc82-48b0-86ec-3b0755de7515/data)."
        )

        providers_raw = fetch_provider_data(limit=5000)
        if not providers_raw:
            st.info("No provider data available. The API may be temporarily unavailable.")
        else:
            prov_df = pd.DataFrame(providers_raw)

            col1, col2 = st.columns(2)
            with col1:
                search_name = st.text_input(
                    "Search by name",
                    placeholder="First name, last name, or organization...",
                    key="provider_name_search",
                )
            with col2:
                provider_types = ["All"] + sorted(
                    prov_df["PROVIDER_TYPE_DESC"].dropna().astype(str).unique().tolist()
                )
                search_type = st.selectbox(
                    "Filter by provider type",
                    provider_types,
                    key="provider_type_search",
                )

            mask = pd.Series(True, index=prov_df.index)
            if search_name:
                search_name_upper = search_name.upper().strip()
                name_cols = ["FIRST_NAME", "LAST_NAME", "ORG_NAME"]
                name_mask = pd.Series(False, index=prov_df.index)
                for col in name_cols:
                    if col in prov_df.columns:
                        name_mask |= prov_df[col].fillna("").astype(str).str.upper().str.contains(search_name_upper, regex=False)
                mask &= name_mask
            if search_type != "All":
                mask &= prov_df["PROVIDER_TYPE_DESC"].astype(str) == search_type

            results = prov_df[mask]
            st.metric("Results", f"{len(results):,}")

            display_cols = ["PROVIDER_TYPE_DESC", "LAST_NAME", "FIRST_NAME", "ORG_NAME", "STATE_CD", "NPI"]
            display_cols = [c for c in display_cols if c in results.columns]
            if display_cols:
                st.dataframe(results[display_cols], use_container_width=True, height=400)
            else:
                st.dataframe(results, use_container_width=True, height=400)

    st.sidebar.caption("Data: CMS MDPP Supplier Mapping; CMS Program Statistics – Medicare Advantage; CMS Provider API")


if __name__ == "__main__":
    main()
