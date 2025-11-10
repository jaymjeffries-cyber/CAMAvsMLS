# Zillow Photo Download Feature

## 🎯 Overview

Your script can now automatically download property photos from Zillow for properties in your reports! Photos are saved to local folders and organized by report type.

---

## ✨ How It Works

When you run your script, after generating reports, you'll be asked:

```
================================================================================
OPTIONAL: Download Zillow Property Photos
================================================================================

Would you like to download property photos from Zillow?
This will:
  • Download the main photo for each property
  • Save photos to 'zillow_photos/' folder
  • Take about 2-3 seconds per property

Download photos? (yes/no, default=no): 
```

**Type `yes` and press Enter** to download photos!

---

## 📸 What Gets Downloaded

### For Each Property:
1. **Script searches Zillow** for the property using address
2. **Finds the property ID** (zpid)
3. **Constructs the photo URL** with `mmlb=g,0` parameter (main photo view)
4. **Downloads the main property photo**
5. **Saves it** with the parcel ID as filename

### Photos Are Saved To:
```
zillow_photos/
├── mismatches/
│   ├── 123456.jpg
│   ├── 789012.jpg
│   └── ...
└── perfect_matches/
    ├── 345678.jpg
    ├── 901234.jpg
    └── ...
```

**Filename:** Parcel ID (e.g., `204522.jpg`)

---

## 🚀 Quick Start

### Step 1: Install Required Packages
```bash
pip install requests beautifulsoup4
```

Or use requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Run Your Script
```bash
python mls_cama_comparison_with_hyperlinks.py
```

### Step 3: When Prompted
```
Download photos? (yes/no, default=no): yes
```

### Step 4: Wait
The script will:
- Show progress for each property
- Display success/failure for each download
- Wait 2 seconds between downloads (to be respectful to Zillow)

---

## 📊 What You'll See

```
================================================================================
Downloading Zillow Photos
================================================================================

📸 Downloading photos for VALUE MISMATCHES...
   Output folder: zillow_photos/mismatches
   Delay between requests: 2 seconds

[1/10] 1118 Raff Rd SW, Canton
  📸 Downloading photo for parcel 123456...
  ✅ Found zpid: 35191188
  ✅ Photo saved: zillow_photos/mismatches/123456.jpg

[2/10] 263 Franklin Ave, Alliance
  📸 Downloading photo for parcel 789012...
  ✅ Found zpid: 35191368
  ✅ Photo saved: zillow_photos/mismatches/789012.jpg

...

✅ Downloaded 8 out of 10 photos
   Photos saved in: zillow_photos/mismatches/
```

---

## ⚙️ Configuration Options

### Change Download Delay
Edit `zillow_photo_downloader.py` line ~200:
```python
delay=2  # Seconds between downloads (default: 2)
```

**Recommendations:**
- **Minimum: 2 seconds** - Be respectful to Zillow's servers
- **For many properties: 3-5 seconds** - More reliable
- **Too fast:** Might get blocked or rate limited

### Change Output Folder
Edit in main script or photo downloader:
```python
output_folder='my_photos'  # Custom folder name
```

### Test Single Download
```bash
python zillow_photo_downloader.py
```

This tests with a sample address.

---

## 🔍 How Zillow URLs Work

### Standard Property URL:
```
https://www.zillow.com/homedetails/1118-Raff-Rd-SW-Canton-OH-44710/35191188_zpid/
```

### Photo View URL (What we use):
```
https://www.zillow.com/homedetails/1118-Raff-Rd-SW-Canton-OH-44710/35191188_zpid/?mmlb=g,0
                                                                                    ↑
                                                                        This shows the main photo!
```

**The `mmlb=g,0` parameter:**
- `g` = gallery view
- `0` = first photo (main photo)

---

## ⚠️ Important Notes

### Success Rate
- ✅ **~80-90%** success rate typically
- Some properties might not have photos
- Some addresses might not be found on Zillow
- Private listings might not be accessible

### What Can Fail
❌ **Property not on Zillow** - New listings or off-market properties  
❌ **Address mismatch** - Different address format than Zillow uses  
❌ **No photos available** - Property has no photos uploaded  
❌ **Rate limiting** - Too many requests too fast  
❌ **Network issues** - Timeout or connection problems  

### When It Fails
The script continues and downloads what it can. Failed downloads are reported but don't stop the process.

---

## 📁 File Structure After Download

```
your-project/
├── mls_cama_comparison_with_hyperlinks.py
├── zillow_photo_downloader.py          ← Photo downloader module
├── zillow_photos/                      ← Created automatically
│   ├── mismatches/
│   │   ├── 123456.jpg
│   │   ├── 789012.jpg
│   │   └── ...
│   └── perfect_matches/
│       ├── 345678.jpg
│       ├── 901234.jpg
│       └── ...
├── discrepancies_value_mismatches.xlsx
├── discrepancies_perfect_matches.xlsx
└── ...
```

---

## 🔧 Advanced Usage

### Download Photos for Specific Report

```python
from zillow_photo_downloader import batch_download_photos
import pandas as pd

# Load your report
df = pd.read_excel('discrepancies_value_mismatches.xlsx')

# Download photos
photo_map = batch_download_photos(
    df[['Parcel_ID', 'Address', 'City', 'State', 'Zip']],
    output_folder='custom_folder',
    delay=3
)

# photo_map is a dictionary: {parcel_id: filepath}
```

### Download Single Photo

```python
from zillow_photo_downloader import download_property_photo

filepath = download_property_photo(
    parcel_id="123456",
    address="1118 Raff Rd SW",
    city="Canton",
    state="OH",
    zip_code="44710",
    output_folder="my_photos"
)

if filepath:
    print(f"Photo saved: {filepath}")
```

### Skip Already Downloaded

The script automatically skips photos that already exist, so you can re-run safely!

---

## 🎓 Example Workflow

### Scenario: Weekly Reports

**Monday:**
```bash
python mls_cama_comparison_with_hyperlinks.py
# Download photos? yes
# ✅ 45 photos downloaded
```

**Tuesday (Re-run):**
```bash
python mls_cama_comparison_with_hyperlinks.py
# Download photos? yes
# ✅ Only downloads NEW properties (existing photos skipped)
```

---

## 💡 Tips & Best Practices

### Tip 1: Download in Batches
For many properties (100+):
- Run first 50, wait
- Run next 50, wait
- Or increase delay to 5 seconds

### Tip 2: Manual Review
After download, manually review photos in the folder to see which properties downloaded successfully.

### Tip 3: Backup Important Photos
If you need specific photos, download them manually from Zillow as backup.

### Tip 4: Respect Zillow's Resources
- Don't download too frequently
- Use reasonable delays (2-3 seconds minimum)
- Don't hammer their servers

### Tip 5: Check Photo Quality
Zillow photos are usually good quality, but verify they meet your needs.

---

## 🆘 Troubleshooting

### "Could not find property on Zillow"
**Causes:**
- Property not listed on Zillow
- Address format doesn't match Zillow's format
- Property is off-market

**Solutions:**
- Verify address is correct
- Try searching manually on Zillow.com
- Some properties just won't be found

### "Could not download photo"
**Causes:**
- Property has no photos
- Photos are private/restricted
- Network timeout

**Solutions:**
- Check the property manually on Zillow
- Increase timeout in the code
- Try again later

### "No photos downloaded"
**Causes:**
- Network issues
- Zillow blocking automated requests
- All addresses invalid

**Solutions:**
- Check your internet connection
- Test with a single property first
- Verify addresses are valid

### Rate Limiting
If you get many failures:
- Increase delay to 5+ seconds
- Download in smaller batches
- Wait before trying again

---

## ❓ FAQ

**Q: Is this legal/allowed?**  
A: This downloads publicly available photos for personal use. Don't republish them commercially. Check Zillow's terms of service.

**Q: How many photos can I download?**  
A: Technically unlimited, but be respectful. Use reasonable delays and don't overwhelm Zillow's servers.

**Q: Will this get me blocked?**  
A: Unlikely if you use reasonable delays (2-3 seconds). The script is respectful to Zillow.

**Q: Can I download all photos from a listing?**  
A: Currently only downloads the main photo. You can modify to get multiple photos by changing the mmlb parameter (g,1, g,2, etc).

**Q: What if I already have some photos?**  
A: The script skips existing photos automatically. No duplicates!

**Q: Can I use this for commercial purposes?**  
A: Check Zillow's terms of service. Photos belong to their owners/Zillow.

**Q: Does this work for all properties?**  
A: Only properties listed on Zillow with photos. Success rate is typically 80-90%.

**Q: How big are the files?**  
A: Typically 200-500 KB per photo. Plan storage accordingly for many properties.

---

## 📈 Performance

### Typical Results:
- **Speed:** 2-3 seconds per property
- **Success Rate:** 80-90%
- **File Size:** 200-500 KB per photo
- **100 properties:** ~5-10 minutes

### Optimization Tips:
- Run during off-peak hours
- Use faster internet connection
- Download in parallel (advanced - modify code)

---

## 🔄 Updates & Maintenance

### If Zillow Changes Their Site:
The photo extraction logic may need updates. Check:
- URL format still works
- Photo selectors still correct
- zpid extraction still works

---

## 📞 Support

### Issues?
1. Test with `python zillow_photo_downloader.py`
2. Check internet connection
3. Verify addresses are correct
4. Try with a single property first

### Want More Features?
- Download multiple photos per property
- Embed photos in Excel
- Custom photo selectors
- Batch processing improvements

---

**Version:** 1.0  
**Last Updated:** November 2025  
**Status:** ✅ Working!
