import streamlit as st
import pandas as pd
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Metiri Payroll Importer", page_icon="💰", layout="wide")

st.title("💰 Metiri Payroll Automation")
st.markdown("""
### Instructions:
1. Upload the **Codes Mapping** file (Excel).
2. Upload the **Employee Deductions** file (Excel).
3. Select columns and download the TXT.
""")

st.divider() # Visual separation line

# --- STEP 1: UPLOAD FILES (Side by Side) ---
col1, col2 = st.columns(2)

with col1:
    st.info("📂 **Step 1: Mapping File**")
    # ADDED key="mapping" to prevent conflict
    codes_file = st.file_uploader("Upload deduction_codes.xlsx", type=["xlsx"], key="mapping")

with col2:
    st.info("📂 **Step 2: Employee Data**")
    # ADDED key="raw_data" to prevent conflict
    data_file = st.file_uploader("Upload employee_deductions.xlsx", type=["xlsx"], key="raw_data")

# --- STEP 2: CONFIGURATION (Sidebar) ---
st.sidebar.header("⚙️ Settings")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("today").replace(day=1))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

# Format dates
str_start_date = start_date.strftime("%Y/%m/%d")
str_end_date = end_date.strftime("%Y/%m/%d")

# --- MAIN LOGIC ---
if data_file and codes_file:
    try:
        # Load files
        df_deductions = pd.read_excel(data_file)
        df_codes = pd.read_excel(codes_file)
        
        st.success(f"✅ Both files loaded! Found {len(df_deductions)} rows.")
        st.divider()

        # --- DYNAMIC COLUMN SELECTION ---
        st.subheader("🛠️ Column Mapping")
        
        all_columns = df_deductions.columns.tolist()
        
        # Smart detection of ID column
        id_index = 0
        if "CI" in all_columns:
            id_index = all_columns.index("CI")
            
        c1, c2 = st.columns(2)
        with c1:
            id_col = st.selectbox("Select ID Column (CI/Legajo)", options=all_columns, index=id_index)
        
        with c2:
            # Default to all columns EXCEPT the ID column
            default_deductions = [c for c in all_columns if c != id_col]
            deduction_cols = st.multiselect("Select Deduction Columns", options=default_deductions, default=default_deductions)

        # --- PROCESSING BUTTON ---
        if st.button("🚀 Generate Metiri TXT", type="primary"):
            
            # 1. PROCESS DATA
            cols_to_keep = [id_col] + deduction_cols
            df_processed = df_deductions[cols_to_keep].fillna(0)

            # 2. MELT
            df_melted = pd.melt(
                df_processed,
                id_vars=[id_col],
                var_name="descuento",
                value_name="Importe"
            )

            # 3. FILTER & MERGE
            df_melted = df_melted[df_melted["Importe"] != 0]
            
            df_final = pd.merge(
                df_melted, 
                df_codes, 
                how="left", 
                left_on="descuento", 
                right_on="descuento"
            )

            # 4. VALIDATION
            unmapped = df_final[df_final["codDescuento"].isna()]
            if not unmapped.empty:
                st.error(f"🛑 STOP: These concepts are missing in your Codes file: {list(unmapped['descuento'].unique())}")
                st.stop()

            # 5. FORMATTING
            output = df_final.copy()
            # Constructing the exact Metiri structure
            # We create a new clean dataframe to avoid index issues
            export_df = pd.DataFrame()
            export_df["vaciaUno"] = [""] * len(output)
            export_df["CI"] = output[id_col]
            export_df["vaciaDos"] = [""] * len(output)
            export_df["fechaInicio"] = str_start_date
            export_df["codDescuento"] = output["codDescuento"]
            export_df["cantidad"] = 1
            export_df["Importe"] = output["Importe"]
            export_df["cuotasInicio"] = 1
            export_df["fechaFin"] = str_end_date
            export_df["cuotasFin"] = 1

            # 6. DOWNLOAD
            buffer = io.BytesIO()
            export_df.to_csv(buffer, sep=";", index=False, header=False, encoding='utf-8')
            buffer.seek(0)
            
            st.balloons() # Fun animation on success
            st.download_button(
                label="📥 Download Final TXT",
                data=buffer,
                file_name="novedades_metiri.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.warning("waiting for files...")