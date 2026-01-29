# UniManage - University Management System

A fully responsive web-based University Management System for managing students, faculty, courses, and departments with support for Google Sheets and Excel data storage.

## 🌟 Features

### Core Functionality
- **Dashboard**: Real-time statistics and top students by GPA
- **Student Management**: Add, edit, delete, and search students with GPA calculation
- **Faculty Management**: Manage faculty members and course assignments
- **Course Management**: Create courses, assign faculty, and enroll students
- **Department Management**: Organize departments with heads and course lists
- **Search & Filter**: Real-time search across all entities
- **Data Persistence**: Multiple storage options (Local Storage, Google Sheets, Excel)

### Data Storage Options

#### 1. Local Storage (Default)
- Data stored in browser's localStorage
- Instant save/load
- Works offline
- No setup required

#### 2. Google Sheets Integration
- Real-time cloud sync
- Collaborative access
- Automatic backups

#### 3. Excel File Import/Export
- Import existing Excel data
- Export all data to Excel format
- Offline file management

### Additional Features
- **Sample Data**: Load pre-filled sample data for testing
- **CSV Export**: Export all data to CSV format
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Real-time GPA Calculation**: Automatic GPA computation based on grades
- **Data Validation**: Form validation for all inputs
- **Toast Notifications**: User-friendly success/error messages

## 🚀 Getting Started

### Basic Setup (Local Storage)

1. **Download the files**:
   - `index.html`
   - `styles.css`
   - `app.js`

2. **Open in browser**:
   - Simply open `index.html` in any modern web browser
   - No server required!

3. **Load sample data** (optional):
   - Go to Settings
   - Click "Load Sample Data"
   - Start exploring the features

### Google Sheets Integration Setup

#### Prerequisites
- Google account
- Google Cloud Platform account (free tier works)

#### Step 1: Create a Google Sheets Spreadsheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Create 5 sheets with these exact names:
   - `Students`
   - `Faculty`
   - `Courses`
   - `Departments`
   - `University`

4. **Students Sheet** - Add headers in row 1:
   ```
   ID | Name | Age | Gender | Department | Courses | Grades
   ```

5. **Faculty Sheet** - Add headers in row 1:
   ```
   ID | Name | Department | Courses Taught
   ```

6. **Courses Sheet** - Add headers in row 1:
   ```
   ID | Name | Credit Hours | Faculty | Students
   ```

7. **Departments Sheet** - Add headers in row 1:
   ```
   ID | Name | Head | Courses
   ```

8. **University Sheet** - Add headers in row 1:
   ```
   Name | Address
   ```

9. Note your Spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit
   ```

#### Step 2: Enable Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one
3. Enable Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

#### Step 3: Create API Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "API Key"
3. Copy your API key
4. Restrict your API key (recommended):
   - Click on the API key
   - Under "Application restrictions": Select "HTTP referrers"
   - Add your domain (or `localhost` for testing)
   - Under "API restrictions": Select "Restrict key"
   - Choose "Google Sheets API"
   - Save

#### Step 4: Make Spreadsheet Public (for API access)

1. Open your Google Sheet
2. Click "Share" button
3. Under "General access": Change to "Anyone with the link"
4. Set permission to "Viewer"
5. Click "Done"

#### Step 5: Configure in UniManage

1. Open UniManage
2. Go to Settings
3. Select "Google Sheets" as storage type
4. Enter your API Key
5. Enter your Spreadsheet ID
6. Click "Test Connection"

**Important Notes:**
- API calls are limited by Google's quota (100 requests per 100 seconds per user)
- For production use, consider OAuth 2.0 instead of API keys
- Keep your API key secure - don't commit to public repositories

### Excel File Integration Setup

#### Using Excel Files

1. **Import from Excel**:
   - Go to Settings
   - Select "Excel File" as storage type
   - Click "Choose File" under "Import Excel File"
   - Select your .xlsx or .xls file
   - Data will be automatically imported

2. **Export to Excel**:
   - Click "Export to Excel" button
   - File `university_data.xlsx` will be downloaded
   - Contains all data in separate sheets

#### Excel File Structure

Your Excel file should have these sheets:

**Students Sheet:**
| ID | Name | Age | Gender | Department | GPA | Courses | Grades |
|----|------|-----|--------|------------|-----|---------|--------|

**Faculty Sheet:**
| ID | Name | Department | Courses Taught |
|----|------|------------|----------------|

**Courses Sheet:**
| ID | Name | Credit Hours | Assigned Faculty | Enrolled Students |
|----|------|--------------|------------------|-------------------|

**Departments Sheet:**
| ID | Name | Head of Department | Total Courses |
|----|------|--------------------|---------------|

**University Sheet:**
| Name | Address | Total Students | Total Faculty | Total Courses | Total Departments |
|------|---------|----------------|---------------|---------------|-------------------|

## 📱 Responsive Design

The system is fully responsive and works on:
- **Desktop**: Full features with optimal layout
- **Tablet**: Adapted layouts for medium screens
- **Mobile**: Mobile-first design with touch-friendly controls

### Mobile Features
- Hamburger menu for navigation
- Scrollable tables
- Touch-optimized buttons
- Stacked forms for easy input

## 🎨 Design Features

### Visual Design
- Academic-inspired color scheme with burgundy and gold
- Elegant serif typography (Cormorant Garamond) for headings
- Clean sans-serif (Work Sans) for body text
- Smooth animations and transitions
- Professional card-based layouts

### User Experience
- Intuitive navigation
- Real-time search and filtering
- Modal dialogs for forms
- Toast notifications for feedback
- Confirmation dialogs for deletions

## 💻 Technical Details

### Technologies Used
- **HTML5**: Semantic markup
- **CSS3**: 
  - CSS Grid and Flexbox for layouts
  - CSS Variables for theming
  - Animations and transitions
  - Media queries for responsiveness
- **JavaScript (ES6+)**:
  - Classes and modules
  - Async/await for API calls
  - LocalStorage API
  - File API for Excel import

### External Libraries
- **SheetJS (xlsx)**: Excel file handling
- CDN: `https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js`

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Opera

## 🔧 Usage Guide

### Adding a Student

1. Go to "Students" section
2. Click "+ Add Student"
3. Fill in required fields:
   - Student ID (unique)
   - Name
   - Age
   - Gender
   - Department
4. Select enrolled courses (optional)
5. Click "Save"

### Editing a Student

1. Find student in the table
2. Click "Edit" button
3. Modify details
4. Add grades for enrolled courses
5. Click "Save"

### Assigning Courses

**To Student:**
1. Edit student
2. Check courses to enroll
3. Add grades for each course
4. GPA is automatically calculated

**To Faculty:**
1. Create/Edit course
2. Select faculty from dropdown
3. Faculty's course list is automatically updated

### Calculating GPA

- GPA is automatically calculated based on course grades
- Scale: 0.0 - 4.0
- Formula: Average of all course grades
- Displayed in student listings and dashboard

### Searching

Use the search boxes to find:
- Students by name or ID
- Faculty by name or ID
- Courses by name or ID

Results update in real-time as you type.

## 📊 Sample Data

The system includes comprehensive sample data:
- 5 Students across different departments
- 5 Faculty members
- 8 Courses
- 4 Departments
- University information

Load sample data from Settings to explore all features.

## 🔒 Data Privacy

### Local Storage
- Data stored only in your browser
- Not accessible by other websites
- Cleared when browser data is cleared

### Google Sheets
- Data stored in your Google account
- Access controlled by sharing settings
- Subject to Google's privacy policy

### Excel Files
- Data stored in local files
- Complete user control
- No cloud sync unless manually uploaded

## 🐛 Troubleshooting

### Google Sheets Issues

**"Error loading from Google Sheets"**
- Check your API key is correct
- Verify spreadsheet ID
- Ensure spreadsheet is shared publicly
- Check API quota hasn't been exceeded

**Data not updating**
- Refresh the page
- Check network connection
- Verify API credentials

### Excel Issues

**"Error importing Excel file"**
- Ensure file is .xlsx or .xls format
- Check sheet names match exactly
- Verify column headers are correct

### General Issues

**Data not saving**
- Check browser localStorage isn't disabled
- Verify sufficient storage space
- Try a different browser

**Forms not submitting**
- Fill all required fields (marked with *)
- Check data validation (e.g., age range, GPA scale)

## 🚀 Deployment

### GitHub Pages
1. Create a GitHub repository
2. Upload all files
3. Go to Settings > Pages
4. Select source branch
5. Your site will be available at: `https://yourusername.github.io/repo-name`

### Other Hosting
Simply upload all files to any web hosting service:
- Netlify
- Vercel
- Firebase Hosting
- Any traditional web host

No server-side code required!

## 📝 Code Structure

```
university-management-system/
│
├── index.html          # Main HTML structure
├── styles.css          # All styling and responsive design
├── app.js             # Core application logic
│   ├── Data Models    # Student, Faculty, Course, Department classes
│   ├── DataManager    # Storage and API integration
│   └── UIManager      # UI updates and event handling
│
└── README.md          # This file
```

### Key Classes

**Student**: Manages student data and GPA calculation
**Faculty**: Manages faculty members and their courses
**Course**: Handles course information and enrollments
**Department**: Department structure and courses
**DataManager**: Handles all data storage (local/Google/Excel)
**UIManager**: Manages all UI interactions and updates

## 🎯 Future Enhancements

Potential features for expansion:
- User authentication and roles
- Grade analytics and reports
- Attendance tracking
- Fee management
- Email notifications
- PDF report generation
- Multi-language support
- Dark mode theme

## 📄 License

This project is open-source and available for educational purposes.

## 👨‍💻 Support

For issues or questions:
1. Check this README first
2. Review the troubleshooting section
3. Check browser console for error messages
4. Ensure all prerequisites are met

## 🎓 Educational Use

This system is perfect for:
- University projects
- Learning web development
- Database design practice
- API integration examples
- Responsive design study

---

**Built with ❤️ for educational institutions**

*Version 1.0 - January 2026*
