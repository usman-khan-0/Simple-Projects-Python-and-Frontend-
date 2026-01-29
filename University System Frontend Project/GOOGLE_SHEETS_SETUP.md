# Google Sheets Setup Guide - Detailed Instructions

This guide provides step-by-step instructions to set up Google Sheets integration for the University Management System.

## Table of Contents
1. [Create Google Spreadsheet](#step-1-create-google-spreadsheet)
2. [Enable Google Sheets API](#step-2-enable-google-sheets-api)
3. [Create API Credentials](#step-3-create-api-credentials)
4. [Configure Spreadsheet Access](#step-4-configure-spreadsheet-access)
5. [Connect to UniManage](#step-5-connect-to-unimanage)
6. [Testing & Verification](#step-6-testing--verification)
7. [Troubleshooting](#troubleshooting)

---

## Step 1: Create Google Spreadsheet

### 1.1 Create New Spreadsheet

1. Go to https://sheets.google.com
2. Sign in with your Google account
3. Click the "+" button to create a new spreadsheet
4. Name it "University Management Data" (or any name you prefer)

### 1.2 Create Required Sheets

By default, you'll have one sheet. You need to create 5 sheets total:

1. **Rename the first sheet to "Students"**
   - Right-click on "Sheet1" at the bottom
   - Select "Rename"
   - Type "Students"

2. **Create remaining sheets**
   - Click the "+" button at the bottom-left (next to sheet tabs)
   - Create sheets with these exact names:
     - Faculty
     - Courses
     - Departments
     - University

### 1.3 Set Up Students Sheet

In the "Students" sheet, add headers in row 1 (A1:G1):

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ID | Name | Age | Gender | Department | Courses | Grades |

**Example data (row 2):**
```
STU001 | John Smith | 20 | Male | Computer Science | CS101,MATH101 | {"CS101":3.5,"MATH101":3.8}
```

### 1.4 Set Up Faculty Sheet

In the "Faculty" sheet, add headers in row 1 (A1:D1):

| A | B | C | D |
|---|---|---|---|
| ID | Name | Department | Courses Taught |

**Example data (row 2):**
```
FAC001 | Dr. Sarah Johnson | Computer Science | CS101,CS201
```

### 1.5 Set Up Courses Sheet

In the "Courses" sheet, add headers in row 1 (A1:E1):

| A | B | C | D | E |
|---|---|---|---|---|
| ID | Name | Credit Hours | Faculty | Students |

**Example data (row 2):**
```
CS101 | Introduction to Programming | 3 | FAC001 | STU001,STU002
```

### 1.6 Set Up Departments Sheet

In the "Departments" sheet, add headers in row 1 (A1:D1):

| A | B | C | D |
|---|---|---|---|
| ID | Name | Head | Courses |

**Example data (row 2):**
```
DEPT001 | Computer Science | Dr. Sarah Johnson | CS101,CS201,CS301
```

### 1.7 Set Up University Sheet

In the "University" sheet, add headers in row 1 (A1:B1):

| A | B |
|---|---|
| Name | Address |

**Example data (row 2):**
```
Lincoln University | 123 Academic Ave, Education City
```

### 1.8 Get Spreadsheet ID

1. Look at the URL of your spreadsheet
2. It looks like: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
3. Copy the **SPREADSHEET_ID** part (between `/d/` and `/edit`)
4. Save this ID - you'll need it later

Example:
```
https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                      This is your Spreadsheet ID
```

---

## Step 2: Enable Google Sheets API

### 2.1 Go to Google Cloud Console

1. Visit https://console.cloud.google.com
2. Sign in with the same Google account

### 2.2 Create a New Project (if needed)

1. Click on the project dropdown at the top
2. Click "NEW PROJECT"
3. Enter project name: "UniManage" (or your choice)
4. Click "CREATE"
5. Wait for project creation (about 30 seconds)
6. Select your new project from the dropdown

### 2.3 Enable Google Sheets API

1. In the left sidebar, click "APIs & Services" > "Library"
2. In the search bar, type "Google Sheets API"
3. Click on "Google Sheets API" in the results
4. Click the blue "ENABLE" button
5. Wait for API to enable (about 10 seconds)

---

## Step 3: Create API Credentials

### 3.1 Create API Key

1. In the left sidebar, click "APIs & Services" > "Credentials"
2. Click "CREATE CREDENTIALS" at the top
3. Select "API key"
4. A popup will show your API key
5. **IMPORTANT**: Copy this key immediately and save it securely
6. Click "CLOSE"

### 3.2 Restrict API Key (Recommended for Security)

1. Find your API key in the list
2. Click the pencil icon (Edit) next to it
3. Under "API restrictions":
   - Select "Restrict key"
   - Check only "Google Sheets API"
4. Under "Application restrictions":
   - For testing locally: Select "None"
   - For production: Select "HTTP referrers (web sites)"
     - Add your domain: `https://yourdomain.com/*`
     - For localhost testing: `http://localhost/*`
5. Click "SAVE"

**Your API Key should look like:**
```
AIzaSyD1234567890ABCDEFGhijklmnopQRSTUVW
```

---

## Step 4: Configure Spreadsheet Access

### 4.1 Make Spreadsheet Accessible via API

1. Open your Google Spreadsheet
2. Click the blue "Share" button (top-right)
3. Under "General access":
   - Click "Restricted"
   - Change to "Anyone with the link"
4. Set permission level to "Viewer"
5. Click "Done"

**Security Note:**
- This makes the spreadsheet readable by anyone with the link
- Data can only be viewed, not edited directly
- Only UniManage app with your API key can edit it
- For sensitive data, consider OAuth 2.0 instead

### 4.2 Verify Access

1. Copy the spreadsheet URL
2. Open an incognito/private browser window
3. Paste the URL
4. You should be able to view (but not edit) the spreadsheet

---

## Step 5: Connect to UniManage

### 5.1 Open UniManage

1. Open the UniManage application in your browser
2. Click on "Settings" in the navigation

### 5.2 Configure Storage

1. Under "Data Storage", select "Google Sheets"
2. The Google Sheets configuration form will appear

### 5.3 Enter Credentials

1. **API Key**: Paste your API key from Step 3
   ```
   Example: AIzaSyD1234567890ABCDEFGhijklmnopQRSTUVW
   ```

2. **Spreadsheet ID**: Paste your Spreadsheet ID from Step 1
   ```
   Example: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
   ```

### 5.4 Test Connection

1. Click "Test Connection" button
2. Wait for the response (3-5 seconds)
3. You should see a success message
4. Data from your spreadsheet will be loaded into the app

---

## Step 6: Testing & Verification

### 6.1 Test Reading Data

1. Go to "Dashboard" section
2. Verify statistics match your spreadsheet data
3. Check "Students" section shows your student data
4. Verify all sections load correctly

### 6.2 Test Writing Data

1. Go to "Students" section
2. Click "+ Add Student"
3. Fill in the form:
   - Student ID: TEST001
   - Name: Test Student
   - Age: 20
   - Gender: Male
   - Department: Computer Science
4. Click "Save"
5. Open your Google Spreadsheet
6. Check the "Students" sheet
7. Your new student should appear in the sheet

### 6.3 Test Editing Data

1. In UniManage, click "Edit" on a student
2. Change their name
3. Click "Save"
4. Refresh your Google Spreadsheet
5. The name should be updated

### 6.4 Test Deleting Data

1. In UniManage, click "Delete" on a student
2. Confirm deletion
3. Refresh your Google Spreadsheet
4. The student should be removed

---

## Troubleshooting

### Error: "Error loading from Google Sheets"

**Possible causes:**

1. **Incorrect API Key**
   - Solution: Double-check your API key
   - Make sure there are no extra spaces
   - Verify API is enabled in Google Cloud Console

2. **Incorrect Spreadsheet ID**
   - Solution: Verify the ID from the URL
   - Should be the long string between `/d/` and `/edit`

3. **Spreadsheet not shared**
   - Solution: Make sure "Anyone with the link" can view
   - Check sharing settings in your spreadsheet

4. **API Quota Exceeded**
   - Solution: Google has rate limits
   - Wait a few minutes and try again
   - Check quota in Google Cloud Console

5. **Wrong Sheet Names**
   - Solution: Sheet names must be exactly:
     - Students
     - Faculty
     - Courses
     - Departments
     - University
   - Names are case-sensitive!

### Error: "Failed to save data"

**Possible causes:**

1. **Permission Issues**
   - The API only has viewer permissions by default
   - This is a limitation of API key authentication
   - For write access, you need OAuth 2.0 (advanced)

2. **Network Issues**
   - Check your internet connection
   - Try refreshing the page

### Data appears empty

**Solutions:**

1. Make sure headers are in row 1
2. Data should start in row 2
3. Check for typos in sheet names
4. Verify spreadsheet sharing settings

### API Key Security Warning

**If you see a security warning:**

1. This is normal for unrestricted keys
2. Restrict your API key as shown in Step 3.2
3. For production, use OAuth 2.0 instead
4. Never commit API keys to public repositories

---

## Advanced: OAuth 2.0 Setup (For Production)

For production applications with write access, you should use OAuth 2.0:

### Benefits
- Users authenticate with their own Google account
- More secure than API keys
- Full read/write permissions
- Better for multi-user applications

### Setup Steps (Brief Overview)

1. In Google Cloud Console > Credentials
2. Create OAuth 2.0 Client ID
3. Configure consent screen
4. Download client configuration
5. Implement OAuth flow in JavaScript
6. Use access tokens instead of API key

This requires more complex implementation. For educational/personal use, API key is sufficient.

---

## Best Practices

### Security
1. **Never share your API key publicly**
2. **Restrict API key to specific domains**
3. **Use environment variables for API keys**
4. **Consider OAuth 2.0 for production**
5. **Regularly rotate API keys**

### Performance
1. **Minimize API calls** - batch operations when possible
2. **Cache data locally** - reduce API requests
3. **Handle rate limits** - implement exponential backoff
4. **Monitor quota usage** in Google Cloud Console

### Data Management
1. **Backup your spreadsheet regularly**
2. **Version control** - save copies before major changes
3. **Test with sample data first**
4. **Document your data structure**

---

## Rate Limits & Quotas

Google Sheets API has these limits:

- **Read requests**: 100 per 100 seconds per user
- **Write requests**: 100 per 100 seconds per user
- **Daily quota**: Check in Cloud Console

If you exceed limits:
- Wait for the quota to reset
- Implement request queuing
- Use batch operations
- Consider upgrading quota (paid)

---

## Quick Reference

### Essential Links

- **Google Sheets**: https://sheets.google.com
- **Cloud Console**: https://console.cloud.google.com
- **API Documentation**: https://developers.google.com/sheets/api

### Required Information Checklist

✅ Spreadsheet ID
✅ API Key
✅ Sheet names created (Students, Faculty, Courses, Departments, University)
✅ Headers added to each sheet
✅ Spreadsheet shared (Anyone with link)
✅ Google Sheets API enabled
✅ API key restrictions configured (optional but recommended)

---

## Support & Resources

For more help:
- Google Sheets API Documentation
- Stack Overflow (tag: google-sheets-api)
- Google Cloud Support

---

**Last Updated**: January 2026
**Guide Version**: 1.0

Good luck with your University Management System! 🎓
