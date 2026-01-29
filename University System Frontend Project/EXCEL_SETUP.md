# Excel File Setup Guide

This guide explains how to create and use Excel files with the University Management System.

## Quick Start

### Option 1: Import Sample Excel File

1. Download the sample Excel file (if provided)
2. Open UniManage application
3. Go to Settings
4. Select "Excel File" as storage type
5. Click "Choose File" under "Import Excel File"
6. Select your .xlsx or .xls file
7. Data will be automatically imported

### Option 2: Create Your Own Excel File

Follow the structure below to create a compatible Excel file.

---

## Excel File Structure

Your Excel workbook should contain these 5 sheets (tabs):

1. **Students**
2. **Faculty**
3. **Courses**
4. **Departments**
5. **University**

---

## Sheet 1: Students

### Column Headers (Row 1)

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| ID | Name | Age | Gender | Department | GPA | Courses | Grades |

### Column Descriptions

- **ID**: Unique student identifier (e.g., STU001, STU002)
- **Name**: Full name of the student
- **Age**: Student's age (numeric, typically 16-100)
- **Gender**: Male, Female, or Other
- **Department**: Department name (must match Department sheet)
- **GPA**: Grade Point Average (0.0 - 4.0, calculated automatically)
- **Courses**: Comma-separated course IDs (e.g., CS101,MATH101,PHY101)
- **Grades**: JSON format: {"CS101":3.5,"MATH101":3.8}

### Sample Data

| ID | Name | Age | Gender | Department | GPA | Courses | Grades |
|---|---|---|---|---|---|---|---|
| STU001 | Alice Johnson | 20 | Female | Computer Science | 3.80 | CS101,MATH101,BUS101 | {"CS101":3.7,"MATH101":3.9,"BUS101":3.8} |
| STU002 | Bob Williams | 21 | Male | Computer Science | 3.50 | CS101,CS201,MATH201 | {"CS101":3.5,"CS201":3.6,"MATH201":3.4} |
| STU003 | Carol Davis | 19 | Female | Computer Science | 3.90 | CS101,CS301,PHY201 | {"CS101":4.0,"CS301":3.9,"PHY201":3.8} |
| STU004 | David Miller | 22 | Male | Physics | 3.50 | CS201,PHY101 | {"CS201":3.3,"PHY101":3.7} |
| STU005 | Emma Garcia | 20 | Female | Mathematics | 3.70 | MATH101,PHY101 | {"MATH101":3.8,"PHY101":3.6} |

---

## Sheet 2: Faculty

### Column Headers (Row 1)

| A | B | C | D |
|---|---|---|---|
| ID | Name | Department | Courses Taught |

### Column Descriptions

- **ID**: Unique faculty identifier (e.g., FAC001, FAC002)
- **Name**: Full name with title (e.g., Dr. John Smith)
- **Department**: Department name (must match Department sheet)
- **Courses Taught**: Comma-separated course IDs (e.g., CS101,CS201)

### Sample Data

| ID | Name | Department | Courses Taught |
|---|---|---|---|
| FAC001 | Dr. James Anderson | Computer Science | CS101,CS201 |
| FAC002 | Prof. Lisa Martinez | Computer Science | CS301 |
| FAC003 | Dr. David Kim | Mathematics | MATH101,MATH201 |
| FAC004 | Dr. Emma Thompson | Physics | PHY101,PHY201 |
| FAC005 | Prof. John Smith | Business Administration | BUS101 |

---

## Sheet 3: Courses

### Column Headers (Row 1)

| A | B | C | D | E |
|---|---|---|---|---|
| ID | Name | Credit Hours | Assigned Faculty | Enrolled Students |

### Column Descriptions

- **ID**: Unique course identifier (e.g., CS101, MATH201)
- **Name**: Full course name
- **Credit Hours**: Number of credit hours (typically 1-6)
- **Assigned Faculty**: Faculty ID who teaches this course (or blank if none)
- **Enrolled Students**: Number of enrolled students (numeric) or comma-separated student IDs

### Sample Data

| ID | Name | Credit Hours | Assigned Faculty | Enrolled Students |
|---|---|---|---|---|
| CS101 | Introduction to Programming | 3 | FAC001 | STU001,STU002,STU003 |
| CS201 | Data Structures | 4 | FAC001 | STU002,STU004 |
| CS301 | Algorithms | 4 | FAC002 | STU003 |
| MATH101 | Calculus I | 3 | FAC003 | STU001,STU005 |
| MATH201 | Linear Algebra | 3 | FAC003 | STU002 |
| PHY101 | Physics I | 4 | FAC004 | STU004,STU005 |
| PHY201 | Quantum Mechanics | 4 | FAC004 | STU003 |
| BUS101 | Introduction to Business | 3 | FAC005 | STU001 |

---

## Sheet 4: Departments

### Column Headers (Row 1)

| A | B | C | D |
|---|---|---|---|
| ID | Name | Head | Courses |

### Column Descriptions

- **ID**: Unique department identifier (e.g., DEPT001, DEPT002)
- **Name**: Department name
- **Head**: Head of Department (name)
- **Courses**: Comma-separated course IDs in this department

### Sample Data

| ID | Name | Head | Courses |
|---|---|---|---|
| DEPT001 | Computer Science | Dr. Sarah Johnson | CS101,CS201,CS301 |
| DEPT002 | Mathematics | Dr. Michael Chen | MATH101,MATH201 |
| DEPT003 | Physics | Dr. Emily Davis | PHY101,PHY201 |
| DEPT004 | Business Administration | Dr. Robert Williams | BUS101 |

---

## Sheet 5: University

### Column Headers (Row 1)

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Name | Address | Total Students | Total Faculty | Total Courses | Total Departments |

### Column Descriptions

- **Name**: University name
- **Address**: Full address
- **Total Students**: Count (calculated automatically by app)
- **Total Faculty**: Count (calculated automatically by app)
- **Total Courses**: Count (calculated automatically by app)
- **Total Departments**: Count (calculated automatically by app)

### Sample Data

| Name | Address | Total Students | Total Faculty | Total Courses | Total Departments |
|---|---|---|---|---|---|
| Lincoln University | 123 Academic Ave, Education City, EC 12345 | 5 | 5 | 8 | 4 |

---

## Important Notes

### File Format
- **Supported formats**: .xlsx (Excel 2007+), .xls (Excel 97-2003)
- **Recommended**: .xlsx for better compatibility

### Data Types
- Text fields: Regular text (strings)
- Numeric fields: Numbers without quotes
- JSON fields (Grades): Must be valid JSON format
- Lists (Courses, Students): Comma-separated values, no spaces

### Naming Conventions
- **Sheet names**: Must be exact (case-sensitive)
  - ✅ "Students" 
  - ❌ "students" or "Student"
- **Column headers**: Must match exactly (case-sensitive)
- **IDs**: Can use any format, but should be unique
  - Suggested: PREFIX + NUMBER (e.g., STU001, FAC001)

### Required vs Optional Fields

**Students:**
- Required: ID, Name, Age, Gender, Department
- Optional: Courses, Grades

**Faculty:**
- Required: ID, Name, Department
- Optional: Courses Taught

**Courses:**
- Required: ID, Name, Credit Hours
- Optional: Assigned Faculty, Enrolled Students

**Departments:**
- Required: ID, Name, Head
- Optional: Courses

**University:**
- Required: Name, Address
- Optional: All count fields (auto-calculated)

---

## Creating Excel File Step-by-Step

### Using Microsoft Excel

1. **Open Excel**
   - Create new blank workbook

2. **Create First Sheet (Students)**
   - Rename "Sheet1" to "Students"
   - Add headers in row 1
   - Add your data starting from row 2

3. **Add Remaining Sheets**
   - Right-click sheet tab > Insert > Worksheet
   - Rename to: Faculty, Courses, Departments, University
   - Add headers and data to each

4. **Save File**
   - File > Save As
   - Choose location
   - File name: "university_data.xlsx"
   - Save as type: "Excel Workbook (*.xlsx)"
   - Click Save

### Using Google Sheets (then export to Excel)

1. **Create in Google Sheets**
   - Follow same structure as above
   - Create all 5 sheets
   - Add headers and data

2. **Export to Excel**
   - File > Download > Microsoft Excel (.xlsx)
   - File will download to your computer

3. **Use in UniManage**
   - Upload the downloaded .xlsx file

### Using LibreOffice Calc (Free Alternative)

1. **Download LibreOffice**
   - Visit https://www.libreoffice.org
   - Download and install (free)

2. **Create Spreadsheet**
   - Open LibreOffice Calc
   - Follow same structure as above
   - Create all 5 sheets

3. **Save as Excel Format**
   - File > Save As
   - Format: "Microsoft Excel 2007-2019 (.xlsx)"
   - Save

---

## Data Validation Tips

### Student IDs
```
Format: STU + 3-digit number
Examples: STU001, STU002, STU010, STU100
```

### Faculty IDs
```
Format: FAC + 3-digit number
Examples: FAC001, FAC002, FAC010
```

### Course IDs
```
Format: DEPT_CODE + LEVEL
Examples: CS101, MATH201, PHY301, BUS101
```

### Department IDs
```
Format: DEPT + 3-digit number
Examples: DEPT001, DEPT002, DEPT003
```

### Grades Format (JSON)
```json
Correct: {"CS101":3.5,"MATH101":3.8}
Wrong: {CS101:3.5,MATH101:3.8}
Wrong: CS101:3.5,MATH101:3.8
```

### Course Lists
```
Correct: CS101,MATH101,PHY101
Wrong: CS101, MATH101, PHY101 (no spaces)
Wrong: CS101;MATH101;PHY101 (use commas)
```

---

## Importing Your Excel File

### Step-by-Step Import

1. **Open UniManage**
   - Launch the application in your browser

2. **Go to Settings**
   - Click "Settings" in navigation

3. **Select Excel Storage**
   - Under "Data Storage"
   - Select "Excel File" radio button

4. **Choose File**
   - Click "Choose File" under "Import Excel File"
   - Navigate to your Excel file
   - Click "Open"

5. **Automatic Import**
   - Data will be imported automatically
   - Success message will appear
   - Go to Dashboard to verify import

### Verification

After import, check:
- ✅ Dashboard shows correct counts
- ✅ Students appear in Students section
- ✅ Faculty appears in Faculty section
- ✅ Courses appear in Courses section
- ✅ Departments appear in Departments section
- ✅ University info shows in Dashboard

---

## Exporting Data to Excel

### Export Process

1. **Go to Settings**
2. **Click "Export to Excel"**
3. **File Downloads**
   - Name: "university_data.xlsx"
   - Location: Your default download folder

### Exported File Contents

The exported file includes:
- All students with complete information
- All faculty members
- All courses with enrollments
- All departments
- University information with statistics

### Use Cases for Export

- **Backup**: Regular data backups
- **Analysis**: Use Excel for advanced analytics
- **Sharing**: Share data with colleagues
- **Reporting**: Create reports in Excel
- **Migration**: Move data to other systems

---

## Troubleshooting

### "Error importing Excel file"

**Possible causes:**

1. **Wrong file format**
   - Solution: Make sure it's .xlsx or .xls
   - Try saving in Excel 2007+ format

2. **Sheet names don't match**
   - Solution: Names must be exact:
     - Students (not Student or students)
     - Faculty (not Faculties)
     - Courses (not Course)
     - Departments (not Department)
     - University

3. **Missing headers**
   - Solution: Row 1 must have all column headers
   - Check spelling and capitalization

4. **Corrupted file**
   - Solution: Try opening in Excel first
   - Save a fresh copy
   - Try again

### Data not appearing correctly

**Solutions:**

1. **Check data types**
   - Numbers should be numbers, not text
   - JSON must be valid format
   - Lists must be comma-separated

2. **Remove extra spaces**
   - Course lists: "CS101,CS201" not "CS101, CS201"
   - IDs should have no leading/trailing spaces

3. **Verify relationships**
   - Course IDs in Students must exist in Courses sheet
   - Faculty IDs in Courses must exist in Faculty sheet
   - Department names must match exactly

### Export file is empty

**Solutions:**

1. Add some data first
2. Try "Load Sample Data" button
3. Check browser console for errors
4. Try a different browser

---

## Sample Excel File

A complete sample Excel file is available with:
- 5 students
- 5 faculty members
- 8 courses
- 4 departments
- Full university information

This sample can be used as a template for your own data.

---

## Best Practices

### Before Import
1. ✅ Backup your existing data
2. ✅ Test with sample file first
3. ✅ Verify all sheet names
4. ✅ Check data formatting
5. ✅ Remove any blank rows

### Data Entry
1. ✅ Use consistent ID formats
2. ✅ Maintain referential integrity
3. ✅ Validate JSON format
4. ✅ No special characters in IDs
5. ✅ Keep data clean and organized

### After Import
1. ✅ Verify all data loaded
2. ✅ Check relationships (students-courses)
3. ✅ Test edit functionality
4. ✅ Export to confirm data
5. ✅ Create backup

---

## Advanced Tips

### Large Datasets
- Split into multiple files if >1000 rows
- Import one sheet at a time
- Use data validation in Excel
- Consider using CSV for very large datasets

### Data Migration
- Export from old system
- Format according to this guide
- Test with small subset first
- Import full dataset

### Automation
- Use Excel formulas for calculations
- Auto-generate IDs with formulas
- Use data validation to prevent errors
- Create drop-down lists for consistency

---

## Quick Reference

### File Requirements Checklist

✅ File format: .xlsx or .xls
✅ 5 sheets: Students, Faculty, Courses, Departments, University
✅ Headers in row 1 of each sheet
✅ Data starts in row 2
✅ All required fields filled
✅ IDs are unique
✅ Relationships are valid (e.g., course IDs exist)
✅ JSON format is valid (for grades)
✅ No extra spaces in data

### Common Issues Quick Fixes

| Issue | Fix |
|-------|-----|
| Sheet not found | Rename sheet to exact name |
| Import fails | Check file format (.xlsx) |
| Missing data | Verify headers match guide |
| Wrong counts | Check for duplicate IDs |
| Invalid JSON | Use format: {"key":value} |

---

**Last Updated**: January 2026  
**Guide Version**: 1.0

Happy data management! 📊
