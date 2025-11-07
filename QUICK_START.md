# Quick Start Guide - MLS vs CAMA Comparison Tool

## For Non-Technical Users

### What You Need
- A Windows, Mac, or Linux computer
- Internet connection (for initial setup only)

---

## 🚀 First Time Setup (5 minutes)

### Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Click the big yellow "Download Python" button
3. Run the installer
4. **IMPORTANT**: Check the box "Add Python to PATH" before clicking Install
5. Click "Install Now"

### Step 2: Install Streamlit
1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
   - Windows: Press Windows key + R, type `cmd`, press Enter
   - Mac: Press Cmd + Space, type `terminal`, press Enter
2. Copy and paste this command and press Enter:
   ```
   pip install streamlit pandas openpyxl
   ```
3. Wait for installation to complete (1-2 minutes)

---

## 🎯 Running the Application

### Easy Method (Windows Only)
1. Double-click the file named `Launch_App.bat`
2. A browser window will open automatically
3. Done! Start using the app

### Manual Method (All Systems)
1. Open Command Prompt or Terminal
2. Navigate to the folder containing the app:
   ```
   cd path/to/your/folder
   ```
3. Run this command:
   ```
   streamlit run mls_cama_app.py
   ```
4. Your browser will open automatically to http://localhost:8501

---

## 📱 Using the Application

### Step-by-Step Usage

1. **Upload Your Files**
   - Click "Browse files" under "Upload MLS Data"
   - Select your MLS Excel file
   - Click "Browse files" under "Upload CAMA Data"
   - Select your CAMA Excel file

2. **Check Settings** (Usually defaults are fine)
   - Make sure column names match your files
   - Default tolerance is 0.01 (works for most cases)

3. **Run the Comparison**
   - Click the big blue "Run Comparison" button
   - Wait for results (usually takes 5-30 seconds)

4. **View Results**
   - See counts of missing records and mismatches
   - Review the summary charts

5. **Download Reports**
   - Click any "Download" button to get Excel files
   - Open Excel files to see results with clickable links
   - **Parcel ID**: Click to open CAMA record
   - **Address**: Click to open Zillow property page

---

## 🛑 Stopping the Application

- Close the browser tab
- In the Command Prompt/Terminal window, press `Ctrl + C`
- Close the Command Prompt/Terminal window

---

## 💾 Tips for Best Results

✅ **Close Excel Files**: Make sure your MLS and CAMA files aren't open in Excel  
✅ **File Format**: Use .xlsx or .xls files only  
✅ **File Size**: Works with files up to 50,000 rows  
✅ **Run Often**: Upload new files anytime to run fresh comparisons  
✅ **Save Reports**: Download and save Excel reports before running a new comparison  

---

## ❗ Common Issues & Solutions

### "Python is not recognized"
**Solution**: You need to install Python (see Step 1 above). Make sure you check "Add Python to PATH"

### "streamlit is not recognized"
**Solution**: Run this command:
```
pip install streamlit
```

### "File not found"
**Solution**: Make sure you're in the correct folder. Use the `cd` command to navigate to where you saved `mls_cama_app.py`

### App Won't Load
**Solution**: 
- Check your internet connection
- Try a different browser
- Make sure port 8501 isn't blocked by firewall

### Excel File Won't Upload
**Solution**:
- Close the file in Excel first
- Make sure it's .xlsx or .xls format
- Try with a smaller file to test

---

## 🎓 Video Tutorial

For a video walkthrough, search YouTube for "Streamlit tutorial" to see how Streamlit apps work.

---

## 📞 Getting Help

**Can't get it working?**
1. Take a screenshot of any error messages
2. Note which step you're stuck on
3. Contact your IT department or the person who provided this tool

---

## 🔄 Updating the App

When you receive a new version:
1. Replace the old `mls_cama_app.py` file with the new one
2. Restart the application
3. That's it!

---

**Remember**: You only need to do the setup steps ONCE. After that, just double-click `Launch_App.bat` to use the app anytime!
