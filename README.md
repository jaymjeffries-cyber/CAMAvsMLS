# MLS vs CAMA Comparison Application

## 🚀 Quick Start

### Option 1: Run Locally (Recommended)

#### Step 1: Install Python
- Download Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

#### Step 2: Install Required Packages
Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:

```bash
pip install streamlit pandas numpy openpyxl
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

#### Step 3: Run the Application
Navigate to the folder containing `mls_cama_app.py` and run:

```bash
streamlit run mls_cama_app.py
```

The application will automatically open in your web browser at `http://localhost:8501`

---

### Option 2: Create a Desktop Shortcut (Windows)

Create a batch file (.bat) to launch the app with a double-click:

1. Create a new text file named `Launch_MLS_CAMA_App.bat`
2. Add this content:

```batch
@echo off
cd /d "%~dp0"
streamlit run mls_cama_app.py
pause
```

3. Save and double-click to run!

---

### Option 3: Create an Executable (Advanced)

To create a standalone executable that doesn't require Python installation:

#### Install PyInstaller:
```bash
pip install pyinstaller
```

#### Create the executable:
```bash
pyinstaller --onefile --windowed mls_cama_app.py
```

Note: Streamlit apps work best when run directly. For true standalone apps, consider using PyQt or tkinter instead.

---

## 📖 How to Use the Application

### 1. Upload Files
- Click "Browse files" in the sidebar
- Upload your MLS Excel file
- Upload your CAMA Excel file

### 2. Configure Settings (Optional)
- **Column Names**: Update if your files use different column names
- **Numeric Tolerance**: Adjust how strict number comparisons should be (default: 0.01)
- **Skip Zero Values**: Enable/disable ignoring zero values in comparisons
- **URL Templates**: Customize hyperlink patterns

### 3. Run Comparison
- Click the **"Run Comparison"** button
- View results summary with counts and charts

### 4. Download Reports
- Each report includes clickable hyperlinks:
  - **Parcel ID** → Links to Stark County CAMA system
  - **Address** → Links to Zillow property search
- Download Excel files for:
  - Missing in CAMA
  - Missing in MLS
  - Value Mismatches
  - Perfect Matches

---

## 🔧 Customization

### Modify Column Comparisons
Edit these sections in `mls_cama_app.py`:

```python
COLUMNS_TO_COMPARE = [
    {'mls_col': 'Above Grade Finished Area', 'cama_col': 'SFLA'},
    # Add more comparisons here
]

COLUMNS_TO_COMPARE_SUM = [
    {'mls_col': 'Below Grade Finished Area', 'cama_cols': ['RECROMAREA', 'FINBSMTAREA', 'UFEATAREA']}
    # Add sum comparisons here
]

COLUMNS_TO_COMPARE_CATEGORICAL = [
    {
        'mls_col': 'Cooling',
        'cama_col': 'HEAT',
        'mls_check_contains': 'Central Air',
        'cama_expected_if_true': 1,
        'cama_expected_if_false': 0,
        'case_sensitive': False
    }
    # Add categorical comparisons here
]
```

### Change Address Column Names
Update the `ADDRESS_COLUMNS` dictionary:

```python
ADDRESS_COLUMNS = {
    'address': 'Your_Address_Column',
    'city': 'Your_City_Column',
    'state': 'Your_State_Column',
    'zip': 'Your_Zip_Column'
}
```

---

## 🌐 Deploy Online (Optional)

### Deploy to Streamlit Cloud (Free)
1. Create a GitHub account and upload your files
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy!

Your app will be accessible via a public URL that you can share with your team.

---

## 🆘 Troubleshooting

### "Command not found: streamlit"
- Make sure Python and pip are installed
- Try: `python -m streamlit run mls_cama_app.py`

### Port Already in Use
- Try a different port: `streamlit run mls_cama_app.py --server.port 8502`

### Excel Files Won't Upload
- Check file format (must be .xlsx or .xls)
- Ensure file isn't open in Excel
- Try reducing file size if very large

### Hyperlinks Don't Work
- Check that Parcel_ID, Address, City, and Zip columns exist in your data
- Verify URL templates are correct

---

## 📊 Features

✅ **Drag-and-drop file uploads**  
✅ **Real-time data comparison**  
✅ **Interactive results dashboard**  
✅ **Excel reports with clickable hyperlinks**  
✅ **Configurable comparison rules**  
✅ **Visual charts and metrics**  
✅ **No code changes needed for basic use**

---

## 💡 Tips

- **Large Files**: The app can handle thousands of records
- **Multiple Runs**: Upload new files anytime to run fresh comparisons
- **Save Settings**: Bookmark the URL to keep your configuration
- **Share Results**: Download Excel files to share with colleagues

---

## 📞 Support

For questions or issues, refer to:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 🔄 Updates

To update the application:
1. Replace `mls_cama_app.py` with the new version
2. Restart the Streamlit server
3. Refresh your browser

---

**Version**: 1.0  
**Last Updated**: November 2025
