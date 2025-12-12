# 💰 Payroll Deductions Automation App

![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?style=for-the-badge&logo=pandas&logoColor=white)

## 📍 Overview
This is a **Web Application** designed to automate the integration of external payroll deductions into the **Metiri ERP system**.

It replaces the manual, error-prone process of editing Excel files with a robust **Drag & Drop interface**. The app takes raw payroll data, validates it against the company's accounting codes, and instantly generates the strict TXT format required for the settlement process.

---

## 🚀 Key Features
* **User-Friendly Interface:** No coding required. Just drag and drop files.
* **Dynamic Mapping:** Automatically maps deduction names (e.g., "Gym") to ERP codes (e.g., "D_200").
* **Data Validation:** Prevents errors by warning the user if a deduction code is missing *before* generating the file.
* **Auto-Formatting:** Handles "Ghost Spaces", missing values, and wide-to-long transformation automatically.

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| `app.py` | **The Application.** Contains the UI (Streamlit) and Logic (Pandas). |
| `requirements.txt` | List of dependencies required to run the app. |
| `deduction_codes.xlsx` | **Configuration File.** The dictionary linking Concepts to System Codes. |
| `employee_deductions.xlsx` | Example input file (Anonymized). |

---

## 🛠 Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/)
* **Backend Logic:** Python (Pandas)
* **Data Handling:** OpenPyXL

---

## ▶️ How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/maxlemos-automation/payroll-deductions-automation-python.git](https://github.com/maxlemos-automation/payroll-deductions-automation-python.git)
    cd payroll-deductions-automation-python
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch the App:**
    ```bash
    streamlit run app.py
    ```
    The app will open automatically in your browser at `http://localhost:8501`.

---

## 🔒 Privacy & Context
* **Real-World Application:** This tool was developed to handle high-volume payroll processing in an enterprise environment (Uruguay).
* **Data Privacy:** All sample data in this repository is mock data generated for demonstration purposes.

---

## 👤 Author
**Max Lemos** | *Automation Specialist & Accountant*
[🔗 GitHub Profile](https://github.com/maxlemos-automation)