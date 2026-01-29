// ====================================
// DATA MODELS
// ====================================

class Student {
    constructor(id, name, age, gender, department, courses = [], grades = {}) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.gender = gender;
        this.department = department;
        this.courses = courses; // Array of course IDs
        this.grades = grades; // Object: {courseId: grade}
    }

    get gpa() {
        if (Object.keys(this.grades).length === 0) return 0;
        const total = Object.values(this.grades).reduce((sum, grade) => sum + grade, 0);
        return (total / Object.keys(this.grades).length).toFixed(2);
    }
}

class Faculty {
    constructor(id, name, department, coursesTaught = []) {
        this.id = id;
        this.name = name;
        this.department = department;
        this.coursesTaught = coursesTaught; // Array of course IDs
    }
}

class Course {
    constructor(id, name, creditHours, assignedFaculty = null, enrolledStudents = []) {
        this.id = id;
        this.name = name;
        this.creditHours = creditHours;
        this.assignedFaculty = assignedFaculty; // Faculty ID
        this.enrolledStudents = enrolledStudents; // Array of student IDs
    }
}

class Department {
    constructor(id, name, headOfDepartment, courses = []) {
        this.id = id;
        this.name = name;
        this.headOfDepartment = headOfDepartment;
        this.courses = courses; // Array of course IDs
    }
}

class University {
    constructor(name = '', address = '') {
        this.name = name;
        this.address = address;
    }
}

// ====================================
// DATA STORAGE MANAGER
// ====================================

class DataManager {
    constructor() {
        this.storageType = 'local'; // 'local', 'google', 'excel'
        this.data = {
            students: [],
            faculty: [],
            courses: [],
            departments: [],
            university: new University()
        };
        this.googleConfig = {
            apiKey: '',
            spreadsheetId: ''
        };
    }

    // Load data from storage
    async loadData() {
        if (this.storageType === 'local') {
            const stored = localStorage.getItem('uniManageData');
            if (stored) {
                const parsed = JSON.parse(stored);
                this.data = {
                    students: parsed.students.map(s => Object.assign(new Student(), s)),
                    faculty: parsed.faculty.map(f => Object.assign(new Faculty(), f)),
                    courses: parsed.courses.map(c => Object.assign(new Course(), c)),
                    departments: parsed.departments.map(d => Object.assign(new Department(), d)),
                    university: Object.assign(new University(), parsed.university || {})
                };
            }
        } else if (this.storageType === 'google') {
            await this.loadFromGoogleSheets();
        }
    }

    // Save data to storage
    async saveData() {
        if (this.storageType === 'local') {
            localStorage.setItem('uniManageData', JSON.stringify(this.data));
        } else if (this.storageType === 'google') {
            await this.saveToGoogleSheets();
        }
    }

    // Google Sheets integration
    async loadFromGoogleSheets() {
        // Note: This requires Google Sheets API setup
        // For demo purposes, we'll show the structure
        try {
            const baseUrl = `https://sheets.googleapis.com/v4/spreadsheets/${this.googleConfig.spreadsheetId}/values`;
            const apiKey = this.googleConfig.apiKey;

            // Fetch each sheet
            const sheets = ['Students', 'Faculty', 'Courses', 'Departments', 'University'];
            
            for (const sheet of sheets) {
                const response = await fetch(`${baseUrl}/${sheet}!A:Z?key=${apiKey}`);
                if (response.ok) {
                    const result = await response.json();
                    this.parseGoogleSheetData(sheet, result.values);
                }
            }
        } catch (error) {
            console.error('Error loading from Google Sheets:', error);
            showToast('Error loading from Google Sheets', 'error');
        }
    }

    parseGoogleSheetData(sheetName, values) {
        if (!values || values.length < 2) return;

        const headers = values[0];
        const rows = values.slice(1);

        switch(sheetName) {
            case 'Students':
                this.data.students = rows.map(row => {
                    const student = new Student(
                        row[0], row[1], parseInt(row[2]), row[3], row[4],
                        row[5] ? row[5].split(',') : [],
                        row[6] ? JSON.parse(row[6]) : {}
                    );
                    return student;
                });
                break;
            case 'Faculty':
                this.data.faculty = rows.map(row => new Faculty(
                    row[0], row[1], row[2], row[3] ? row[3].split(',') : []
                ));
                break;
            case 'Courses':
                this.data.courses = rows.map(row => new Course(
                    row[0], row[1], parseInt(row[2]), row[3], row[4] ? row[4].split(',') : []
                ));
                break;
            case 'Departments':
                this.data.departments = rows.map(row => new Department(
                    row[0], row[1], row[2], row[3] ? row[3].split(',') : []
                ));
                break;
            case 'University':
                if (rows[0]) {
                    this.data.university = new University(rows[0][0], rows[0][1]);
                }
                break;
        }
    }

    async saveToGoogleSheets() {
        try {
            const baseUrl = `https://sheets.googleapis.com/v4/spreadsheets/${this.googleConfig.spreadsheetId}/values`;
            const apiKey = this.googleConfig.apiKey;

            // Prepare data for each sheet
            const sheetsData = {
                'Students': [
                    ['ID', 'Name', 'Age', 'Gender', 'Department', 'Courses', 'Grades'],
                    ...this.data.students.map(s => [
                        s.id, s.name, s.age, s.gender, s.department,
                        s.courses.join(','), JSON.stringify(s.grades)
                    ])
                ],
                'Faculty': [
                    ['ID', 'Name', 'Department', 'Courses Taught'],
                    ...this.data.faculty.map(f => [
                        f.id, f.name, f.department, f.coursesTaught.join(',')
                    ])
                ],
                'Courses': [
                    ['ID', 'Name', 'Credit Hours', 'Faculty', 'Students'],
                    ...this.data.courses.map(c => [
                        c.id, c.name, c.creditHours, c.assignedFaculty || '',
                        c.enrolledStudents.join(',')
                    ])
                ],
                'Departments': [
                    ['ID', 'Name', 'Head', 'Courses'],
                    ...this.data.departments.map(d => [
                        d.id, d.name, d.headOfDepartment, d.courses.join(',')
                    ])
                ],
                'University': [
                    ['Name', 'Address'],
                    [this.data.university.name, this.data.university.address]
                ]
            };

            // Update each sheet
            for (const [sheetName, values] of Object.entries(sheetsData)) {
                const response = await fetch(
                    `${baseUrl}/${sheetName}!A1:clear?key=${apiKey}`,
                    { method: 'POST' }
                );
                
                await fetch(
                    `${baseUrl}/${sheetName}!A1?valueInputOption=RAW&key=${apiKey}`,
                    {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ values })
                    }
                );
            }
            
            showToast('Data saved to Google Sheets successfully', 'success');
        } catch (error) {
            console.error('Error saving to Google Sheets:', error);
            showToast('Error saving to Google Sheets', 'error');
        }
    }

    // Excel integration using SheetJS
    importFromExcel(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = new Uint8Array(e.target.result);
                const workbook = XLSX.read(data, { type: 'array' });

                // Parse each sheet
                ['Students', 'Faculty', 'Courses', 'Departments', 'University'].forEach(sheetName => {
                    if (workbook.SheetNames.includes(sheetName)) {
                        const worksheet = workbook.Sheets[sheetName];
                        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
                        this.parseGoogleSheetData(sheetName, jsonData);
                    }
                });

                this.saveData();
                app.refreshAll();
                showToast('Excel file imported successfully', 'success');
            } catch (error) {
                console.error('Error importing Excel:', error);
                showToast('Error importing Excel file', 'error');
            }
        };
        reader.readAsArrayBuffer(file);
    }

    exportToExcel() {
        try {
            const workbook = XLSX.utils.book_new();

            // Students sheet
            const studentsData = [
                ['ID', 'Name', 'Age', 'Gender', 'Department', 'GPA', 'Courses', 'Grades'],
                ...this.data.students.map(s => [
                    s.id, s.name, s.age, s.gender, s.department, s.gpa,
                    s.courses.join(', '), JSON.stringify(s.grades)
                ])
            ];
            const studentsSheet = XLSX.utils.aoa_to_sheet(studentsData);
            XLSX.utils.book_append_sheet(workbook, studentsSheet, 'Students');

            // Faculty sheet
            const facultyData = [
                ['ID', 'Name', 'Department', 'Courses Taught'],
                ...this.data.faculty.map(f => [
                    f.id, f.name, f.department, f.coursesTaught.join(', ')
                ])
            ];
            const facultySheet = XLSX.utils.aoa_to_sheet(facultyData);
            XLSX.utils.book_append_sheet(workbook, facultySheet, 'Faculty');

            // Courses sheet
            const coursesData = [
                ['ID', 'Name', 'Credit Hours', 'Assigned Faculty', 'Enrolled Students'],
                ...this.data.courses.map(c => [
                    c.id, c.name, c.creditHours, c.assignedFaculty || 'N/A',
                    c.enrolledStudents.length
                ])
            ];
            const coursesSheet = XLSX.utils.aoa_to_sheet(coursesData);
            XLSX.utils.book_append_sheet(workbook, coursesSheet, 'Courses');

            // Departments sheet
            const departmentsData = [
                ['ID', 'Name', 'Head of Department', 'Total Courses'],
                ...this.data.departments.map(d => [
                    d.id, d.name, d.headOfDepartment, d.courses.length
                ])
            ];
            const departmentsSheet = XLSX.utils.aoa_to_sheet(departmentsData);
            XLSX.utils.book_append_sheet(workbook, departmentsSheet, 'Departments');

            // University sheet
            const universityData = [
                ['Name', 'Address', 'Total Students', 'Total Faculty', 'Total Courses', 'Total Departments'],
                [
                    this.data.university.name,
                    this.data.university.address,
                    this.data.students.length,
                    this.data.faculty.length,
                    this.data.courses.length,
                    this.data.departments.length
                ]
            ];
            const universitySheet = XLSX.utils.aoa_to_sheet(universityData);
            XLSX.utils.book_append_sheet(workbook, universitySheet, 'University');

            // Export file
            XLSX.writeFile(workbook, 'university_data.xlsx');
            showToast('Data exported to Excel successfully', 'success');
        } catch (error) {
            console.error('Error exporting to Excel:', error);
            showToast('Error exporting to Excel', 'error');
        }
    }

    exportToCSV() {
        try {
            let csv = 'DATA TYPE,ID,NAME,DETAILS\n';
            
            this.data.students.forEach(s => {
                csv += `Student,${s.id},${s.name},"Age: ${s.age}, Dept: ${s.department}, GPA: ${s.gpa}"\n`;
            });
            
            this.data.faculty.forEach(f => {
                csv += `Faculty,${f.id},${f.name},"Dept: ${f.department}, Courses: ${f.coursesTaught.length}"\n`;
            });
            
            this.data.courses.forEach(c => {
                csv += `Course,${c.id},${c.name},"Credits: ${c.creditHours}, Students: ${c.enrolledStudents.length}"\n`;
            });
            
            this.data.departments.forEach(d => {
                csv += `Department,${d.id},${d.name},"Head: ${d.headOfDepartment}, Courses: ${d.courses.length}"\n`;
            });

            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'university_data.csv';
            a.click();
            
            showToast('Data exported to CSV successfully', 'success');
        } catch (error) {
            console.error('Error exporting to CSV:', error);
            showToast('Error exporting to CSV', 'error');
        }
    }

    loadSampleData() {
        // Sample departments
        this.data.departments = [
            new Department('DEPT001', 'Computer Science', 'Dr. Sarah Johnson', ['CS101', 'CS201', 'CS301']),
            new Department('DEPT002', 'Mathematics', 'Dr. Michael Chen', ['MATH101', 'MATH201']),
            new Department('DEPT003', 'Physics', 'Dr. Emily Davis', ['PHY101', 'PHY201']),
            new Department('DEPT004', 'Business Administration', 'Dr. Robert Williams', ['BUS101', 'BUS201'])
        ];

        // Sample courses
        this.data.courses = [
            new Course('CS101', 'Introduction to Programming', 3, 'FAC001', ['STU001', 'STU002', 'STU003']),
            new Course('CS201', 'Data Structures', 4, 'FAC001', ['STU002', 'STU004']),
            new Course('CS301', 'Algorithms', 4, 'FAC002', ['STU003']),
            new Course('MATH101', 'Calculus I', 3, 'FAC003', ['STU001', 'STU005']),
            new Course('MATH201', 'Linear Algebra', 3, 'FAC003', ['STU002']),
            new Course('PHY101', 'Physics I', 4, 'FAC004', ['STU004', 'STU005']),
            new Course('PHY201', 'Quantum Mechanics', 4, 'FAC004', ['STU003']),
            new Course('BUS101', 'Introduction to Business', 3, 'FAC005', ['STU001'])
        ];

        // Sample faculty
        this.data.faculty = [
            new Faculty('FAC001', 'Dr. James Anderson', 'Computer Science', ['CS101', 'CS201']),
            new Faculty('FAC002', 'Prof. Lisa Martinez', 'Computer Science', ['CS301']),
            new Faculty('FAC003', 'Dr. David Kim', 'Mathematics', ['MATH101', 'MATH201']),
            new Faculty('FAC004', 'Dr. Emma Thompson', 'Physics', ['PHY101', 'PHY201']),
            new Faculty('FAC005', 'Prof. John Smith', 'Business Administration', ['BUS101'])
        ];

        // Sample students
        this.data.students = [
            new Student('STU001', 'Alice Johnson', 20, 'Female', 'Computer Science', 
                ['CS101', 'MATH101', 'BUS101'], {'CS101': 3.7, 'MATH101': 3.9, 'BUS101': 3.8}),
            new Student('STU002', 'Bob Williams', 21, 'Male', 'Computer Science', 
                ['CS101', 'CS201', 'MATH201'], {'CS101': 3.5, 'CS201': 3.6, 'MATH201': 3.4}),
            new Student('STU003', 'Carol Davis', 19, 'Female', 'Computer Science', 
                ['CS101', 'CS301', 'PHY201'], {'CS101': 4.0, 'CS301': 3.9, 'PHY201': 3.8}),
            new Student('STU004', 'David Miller', 22, 'Male', 'Physics', 
                ['CS201', 'PHY101'], {'CS201': 3.3, 'PHY101': 3.7}),
            new Student('STU005', 'Emma Garcia', 20, 'Female', 'Mathematics', 
                ['MATH101', 'PHY101'], {'MATH101': 3.8, 'PHY101': 3.6})
        ];

        // Sample university
        this.data.university = new University('Lincoln University', '123 Academic Ave, Education City, EC 12345');

        this.saveData();
        showToast('Sample data loaded successfully', 'success');
    }

    clearAllData() {
        if (confirm('Are you sure you want to clear all data? This action cannot be undone.')) {
            this.data = {
                students: [],
                faculty: [],
                courses: [],
                departments: [],
                university: new University()
            };
            this.saveData();
            showToast('All data cleared', 'success');
        }
    }
}

// ====================================
// UI MANAGER
// ====================================

class UIManager {
    constructor(dataManager) {
        this.dataManager = dataManager;
        this.currentSection = 'dashboard';
        this.currentEditItem = null;
        this.currentEditType = null;
    }

    init() {
        this.setupNavigation();
        this.setupEventListeners();
        this.setupStorageOptions();
        this.refreshAll();
    }

    setupNavigation() {
        const navButtons = document.querySelectorAll('.nav-btn');
        const mobileToggle = document.getElementById('mobileMenuToggle');
        const mainNav = document.getElementById('mainNav');

        navButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const section = btn.dataset.section;
                this.showSection(section);
                
                navButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Close mobile menu
                mainNav.classList.remove('active');
                mobileToggle.classList.remove('active');
            });
        });

        mobileToggle.addEventListener('click', () => {
            mainNav.classList.toggle('active');
            mobileToggle.classList.toggle('active');
        });
    }

    showSection(sectionId) {
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(sectionId).classList.add('active');
        this.currentSection = sectionId;
        
        // Refresh the section data
        this[`refresh${sectionId.charAt(0).toUpperCase() + sectionId.slice(1)}`]?.();
    }

    setupEventListeners() {
        // Student events
        document.getElementById('addStudentBtn').addEventListener('click', () => this.showAddStudentForm());
        document.getElementById('studentSearch').addEventListener('input', (e) => this.searchTable('students', e.target.value));

        // Faculty events
        document.getElementById('addFacultyBtn').addEventListener('click', () => this.showAddFacultyForm());
        document.getElementById('facultySearch').addEventListener('input', (e) => this.searchTable('faculty', e.target.value));

        // Course events
        document.getElementById('addCourseBtn').addEventListener('click', () => this.showAddCourseForm());
        document.getElementById('courseSearch').addEventListener('input', (e) => this.searchTable('courses', e.target.value));

        // Department events
        document.getElementById('addDepartmentBtn').addEventListener('click', () => this.showAddDepartmentForm());

        // Settings events
        document.getElementById('universityForm').addEventListener('submit', (e) => this.saveUniversityDetails(e));
        document.getElementById('loadSampleData').addEventListener('click', () => {
            this.dataManager.loadSampleData();
            this.refreshAll();
        });
        document.getElementById('exportCSV').addEventListener('click', () => this.dataManager.exportToCSV());
        document.getElementById('clearAllData').addEventListener('click', () => {
            this.dataManager.clearAllData();
            this.refreshAll();
        });
        document.getElementById('exportExcel').addEventListener('click', () => this.dataManager.exportToExcel());
        document.getElementById('excelFile').addEventListener('change', (e) => {
            if (e.target.files[0]) {
                this.dataManager.importFromExcel(e.target.files[0]);
            }
        });

        // Modal events
        document.querySelector('.modal-close').addEventListener('click', () => this.closeModal());
        document.querySelector('.modal-cancel').addEventListener('click', () => this.closeModal());
        document.getElementById('modalForm').addEventListener('submit', (e) => this.handleFormSubmit(e));
        
        // Click outside modal to close
        document.getElementById('modal').addEventListener('click', (e) => {
            if (e.target.id === 'modal') this.closeModal();
        });
    }

    setupStorageOptions() {
        const storageRadios = document.querySelectorAll('input[name="storageType"]');
        storageRadios.forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.dataManager.storageType = e.target.value;
                
                // Show/hide config sections
                document.getElementById('googleSheetsConfig').style.display = 
                    e.target.value === 'google' ? 'block' : 'none';
                document.getElementById('excelConfig').style.display = 
                    e.target.value === 'excel' ? 'block' : 'none';
            });
        });

        document.getElementById('testGoogleConnection').addEventListener('click', async () => {
            this.dataManager.googleConfig.apiKey = document.getElementById('apiKey').value;
            this.dataManager.googleConfig.spreadsheetId = document.getElementById('spreadsheetId').value;
            
            try {
                await this.dataManager.loadFromGoogleSheets();
                showToast('Google Sheets connected successfully', 'success');
                this.refreshAll();
            } catch (error) {
                showToast('Failed to connect to Google Sheets', 'error');
            }
        });
    }

    // ====================================
    // DASHBOARD
    // ====================================

    refreshDashboard() {
        const data = this.dataManager.data;
        
        document.getElementById('totalStudents').textContent = data.students.length;
        document.getElementById('totalFaculty').textContent = data.faculty.length;
        document.getElementById('totalCourses').textContent = data.courses.length;
        document.getElementById('totalDepartments').textContent = data.departments.length;
        
        document.getElementById('uniName').textContent = data.university.name || '—';
        document.getElementById('uniAddress').textContent = data.university.address || '—';

        // Top students
        const topStudents = [...data.students]
            .sort((a, b) => b.gpa - a.gpa)
            .slice(0, 5);

        const tbody = document.querySelector('#topStudentsTable tbody');
        if (topStudents.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No data available</td></tr>';
        } else {
            tbody.innerHTML = topStudents.map((student, index) => `
                <tr>
                    <td>${index + 1}</td>
                    <td>${student.id}</td>
                    <td>${student.name}</td>
                    <td>${student.department}</td>
                    <td>${student.gpa}</td>
                </tr>
            `).join('');
        }
    }

    // ====================================
    // STUDENTS
    // ====================================

    refreshStudents() {
        const tbody = document.querySelector('#studentsTable tbody');
        const students = this.dataManager.data.students;

        if (students.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No students found</td></tr>';
            return;
        }

        tbody.innerHTML = students.map(student => `
            <tr>
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.age}</td>
                <td>${student.gender}</td>
                <td>${student.department}</td>
                <td>${student.gpa}</td>
                <td>
                    <button class="btn-edit" onclick="app.ui.editStudent('${student.id}')">Edit</button>
                    <button class="btn-delete" onclick="app.ui.deleteStudent('${student.id}')">Delete</button>
                </td>
            </tr>
        `).join('');
    }

    showAddStudentForm() {
        const departments = this.dataManager.data.departments.map(d => d.name);
        const courses = this.dataManager.data.courses;
        
        const formHTML = `
            <div class="form-group">
                <label for="studentId">Student ID *</label>
                <input type="text" id="studentId" required>
            </div>
            <div class="form-group">
                <label for="studentName">Name *</label>
                <input type="text" id="studentName" required>
            </div>
            <div class="form-group">
                <label for="studentAge">Age *</label>
                <input type="number" id="studentAge" min="16" max="100" required>
            </div>
            <div class="form-group">
                <label for="studentGender">Gender *</label>
                <select id="studentGender" required>
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                </select>
            </div>
            <div class="form-group">
                <label for="studentDepartment">Department *</label>
                <select id="studentDepartment" required>
                    <option value="">Select Department</option>
                    ${departments.map(d => `<option value="${d}">${d}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Enrolled Courses</label>
                <div id="courseCheckboxes">
                    ${courses.map(c => `
                        <label style="display: block; margin: 5px 0;">
                            <input type="checkbox" name="courses" value="${c.id}">
                            ${c.name} (${c.id})
                        </label>
                    `).join('')}
                </div>
            </div>
        `;

        this.showModal('Add Student', formHTML, 'student');
    }

    editStudent(id) {
        const student = this.dataManager.data.students.find(s => s.id === id);
        if (!student) return;

        const departments = this.dataManager.data.departments.map(d => d.name);
        const courses = this.dataManager.data.courses;
        
        const formHTML = `
            <div class="form-group">
                <label for="studentId">Student ID</label>
                <input type="text" id="studentId" value="${student.id}" readonly>
            </div>
            <div class="form-group">
                <label for="studentName">Name *</label>
                <input type="text" id="studentName" value="${student.name}" required>
            </div>
            <div class="form-group">
                <label for="studentAge">Age *</label>
                <input type="number" id="studentAge" value="${student.age}" min="16" max="100" required>
            </div>
            <div class="form-group">
                <label for="studentGender">Gender *</label>
                <select id="studentGender" required>
                    <option value="Male" ${student.gender === 'Male' ? 'selected' : ''}>Male</option>
                    <option value="Female" ${student.gender === 'Female' ? 'selected' : ''}>Female</option>
                    <option value="Other" ${student.gender === 'Other' ? 'selected' : ''}>Other</option>
                </select>
            </div>
            <div class="form-group">
                <label for="studentDepartment">Department *</label>
                <select id="studentDepartment" required>
                    ${departments.map(d => `
                        <option value="${d}" ${student.department === d ? 'selected' : ''}>${d}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Enrolled Courses</label>
                <div id="courseCheckboxes">
                    ${courses.map(c => `
                        <label style="display: block; margin: 5px 0;">
                            <input type="checkbox" name="courses" value="${c.id}" 
                                ${student.courses.includes(c.id) ? 'checked' : ''}>
                            ${c.name} (${c.id})
                        </label>
                    `).join('')}
                </div>
            </div>
            <div class="form-group">
                <label>Grades (0.0 - 4.0)</label>
                <div id="gradesInputs">
                    ${student.courses.map(courseId => {
                        const course = courses.find(c => c.id === courseId);
                        return `
                            <div style="margin: 8px 0;">
                                <label style="display: inline-block; width: 200px;">${course?.name || courseId}:</label>
                                <input type="number" name="grade_${courseId}" 
                                    value="${student.grades[courseId] || ''}" 
                                    min="0" max="4" step="0.1" 
                                    style="width: 100px;">
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;

        this.currentEditItem = student;
        this.showModal('Edit Student', formHTML, 'student', true);
    }

    deleteStudent(id) {
        if (confirm('Are you sure you want to delete this student?')) {
            this.dataManager.data.students = this.dataManager.data.students.filter(s => s.id !== id);
            
            // Remove from courses
            this.dataManager.data.courses.forEach(course => {
                course.enrolledStudents = course.enrolledStudents.filter(sid => sid !== id);
            });
            
            this.dataManager.saveData();
            this.refreshStudents();
            this.refreshDashboard();
            showToast('Student deleted successfully', 'success');
        }
    }

    // ====================================
    // FACULTY
    // ====================================

    refreshFaculty() {
        const tbody = document.querySelector('#facultyTable tbody');
        const faculty = this.dataManager.data.faculty;

        if (faculty.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No faculty found</td></tr>';
            return;
        }

        tbody.innerHTML = faculty.map(f => `
            <tr>
                <td>${f.id}</td>
                <td>${f.name}</td>
                <td>${f.department}</td>
                <td>${f.coursesTaught.length} courses</td>
                <td>
                    <button class="btn-edit" onclick="app.ui.editFaculty('${f.id}')">Edit</button>
                    <button class="btn-delete" onclick="app.ui.deleteFaculty('${f.id}')">Delete</button>
                </td>
            </tr>
        `).join('');
    }

    showAddFacultyForm() {
        const departments = this.dataManager.data.departments.map(d => d.name);
        
        const formHTML = `
            <div class="form-group">
                <label for="facultyId">Faculty ID *</label>
                <input type="text" id="facultyId" required>
            </div>
            <div class="form-group">
                <label for="facultyName">Name *</label>
                <input type="text" id="facultyName" required>
            </div>
            <div class="form-group">
                <label for="facultyDepartment">Department *</label>
                <select id="facultyDepartment" required>
                    <option value="">Select Department</option>
                    ${departments.map(d => `<option value="${d}">${d}</option>`).join('')}
                </select>
            </div>
        `;

        this.showModal('Add Faculty', formHTML, 'faculty');
    }

    editFaculty(id) {
        const faculty = this.dataManager.data.faculty.find(f => f.id === id);
        if (!faculty) return;

        const departments = this.dataManager.data.departments.map(d => d.name);
        
        const formHTML = `
            <div class="form-group">
                <label for="facultyId">Faculty ID</label>
                <input type="text" id="facultyId" value="${faculty.id}" readonly>
            </div>
            <div class="form-group">
                <label for="facultyName">Name *</label>
                <input type="text" id="facultyName" value="${faculty.name}" required>
            </div>
            <div class="form-group">
                <label for="facultyDepartment">Department *</label>
                <select id="facultyDepartment" required>
                    ${departments.map(d => `
                        <option value="${d}" ${faculty.department === d ? 'selected' : ''}>${d}</option>
                    `).join('')}
                </select>
            </div>
        `;

        this.currentEditItem = faculty;
        this.showModal('Edit Faculty', formHTML, 'faculty', true);
    }

    deleteFaculty(id) {
        if (confirm('Are you sure you want to delete this faculty member?')) {
            this.dataManager.data.faculty = this.dataManager.data.faculty.filter(f => f.id !== id);
            
            // Remove from courses
            this.dataManager.data.courses.forEach(course => {
                if (course.assignedFaculty === id) {
                    course.assignedFaculty = null;
                }
            });
            
            this.dataManager.saveData();
            this.refreshFaculty();
            this.refreshDashboard();
            showToast('Faculty deleted successfully', 'success');
        }
    }

    // ====================================
    // COURSES
    // ====================================

    refreshCourses() {
        const tbody = document.querySelector('#coursesTable tbody');
        const courses = this.dataManager.data.courses;

        if (courses.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No courses found</td></tr>';
            return;
        }

        tbody.innerHTML = courses.map(course => {
            const faculty = this.dataManager.data.faculty.find(f => f.id === course.assignedFaculty);
            return `
                <tr>
                    <td>${course.id}</td>
                    <td>${course.name}</td>
                    <td>${course.creditHours}</td>
                    <td>${faculty ? faculty.name : 'Not assigned'}</td>
                    <td>${course.enrolledStudents.length}</td>
                    <td>
                        <button class="btn-edit" onclick="app.ui.editCourse('${course.id}')">Edit</button>
                        <button class="btn-delete" onclick="app.ui.deleteCourse('${course.id}')">Delete</button>
                    </td>
                </tr>
            `;
        }).join('');
    }

    showAddCourseForm() {
        const faculty = this.dataManager.data.faculty;
        
        const formHTML = `
            <div class="form-group">
                <label for="courseId">Course ID *</label>
                <input type="text" id="courseId" required>
            </div>
            <div class="form-group">
                <label for="courseName">Course Name *</label>
                <input type="text" id="courseName" required>
            </div>
            <div class="form-group">
                <label for="creditHours">Credit Hours *</label>
                <input type="number" id="creditHours" min="1" max="6" required>
            </div>
            <div class="form-group">
                <label for="assignedFaculty">Assigned Faculty</label>
                <select id="assignedFaculty">
                    <option value="">None</option>
                    ${faculty.map(f => `<option value="${f.id}">${f.name} (${f.id})</option>`).join('')}
                </select>
            </div>
        `;

        this.showModal('Add Course', formHTML, 'course');
    }

    editCourse(id) {
        const course = this.dataManager.data.courses.find(c => c.id === id);
        if (!course) return;

        const faculty = this.dataManager.data.faculty;
        
        const formHTML = `
            <div class="form-group">
                <label for="courseId">Course ID</label>
                <input type="text" id="courseId" value="${course.id}" readonly>
            </div>
            <div class="form-group">
                <label for="courseName">Course Name *</label>
                <input type="text" id="courseName" value="${course.name}" required>
            </div>
            <div class="form-group">
                <label for="creditHours">Credit Hours *</label>
                <input type="number" id="creditHours" value="${course.creditHours}" min="1" max="6" required>
            </div>
            <div class="form-group">
                <label for="assignedFaculty">Assigned Faculty</label>
                <select id="assignedFaculty">
                    <option value="">None</option>
                    ${faculty.map(f => `
                        <option value="${f.id}" ${course.assignedFaculty === f.id ? 'selected' : ''}>
                            ${f.name} (${f.id})
                        </option>
                    `).join('')}
                </select>
            </div>
        `;

        this.currentEditItem = course;
        this.showModal('Edit Course', formHTML, 'course', true);
    }

    deleteCourse(id) {
        if (confirm('Are you sure you want to delete this course?')) {
            this.dataManager.data.courses = this.dataManager.data.courses.filter(c => c.id !== id);
            
            // Remove from students
            this.dataManager.data.students.forEach(student => {
                student.courses = student.courses.filter(cid => cid !== id);
                delete student.grades[id];
            });
            
            // Remove from faculty
            this.dataManager.data.faculty.forEach(faculty => {
                faculty.coursesTaught = faculty.coursesTaught.filter(cid => cid !== id);
            });
            
            // Remove from departments
            this.dataManager.data.departments.forEach(dept => {
                dept.courses = dept.courses.filter(cid => cid !== id);
            });
            
            this.dataManager.saveData();
            this.refreshCourses();
            this.refreshDashboard();
            showToast('Course deleted successfully', 'success');
        }
    }

    // ====================================
    // DEPARTMENTS
    // ====================================

    refreshDepartments() {
        const tbody = document.querySelector('#departmentsTable tbody');
        const departments = this.dataManager.data.departments;

        if (departments.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No departments found</td></tr>';
            return;
        }

        tbody.innerHTML = departments.map(dept => `
            <tr>
                <td>${dept.id}</td>
                <td>${dept.name}</td>
                <td>${dept.headOfDepartment}</td>
                <td>${dept.courses.length}</td>
                <td>
                    <button class="btn-edit" onclick="app.ui.editDepartment('${dept.id}')">Edit</button>
                    <button class="btn-delete" onclick="app.ui.deleteDepartment('${dept.id}')">Delete</button>
                </td>
            </tr>
        `).join('');
    }

    showAddDepartmentForm() {
        const formHTML = `
            <div class="form-group">
                <label for="deptId">Department ID *</label>
                <input type="text" id="deptId" required>
            </div>
            <div class="form-group">
                <label for="deptName">Department Name *</label>
                <input type="text" id="deptName" required>
            </div>
            <div class="form-group">
                <label for="deptHead">Head of Department *</label>
                <input type="text" id="deptHead" required>
            </div>
        `;

        this.showModal('Add Department', formHTML, 'department');
    }

    editDepartment(id) {
        const dept = this.dataManager.data.departments.find(d => d.id === id);
        if (!dept) return;
        
        const formHTML = `
            <div class="form-group">
                <label for="deptId">Department ID</label>
                <input type="text" id="deptId" value="${dept.id}" readonly>
            </div>
            <div class="form-group">
                <label for="deptName">Department Name *</label>
                <input type="text" id="deptName" value="${dept.name}" required>
            </div>
            <div class="form-group">
                <label for="deptHead">Head of Department *</label>
                <input type="text" id="deptHead" value="${dept.headOfDepartment}" required>
            </div>
        `;

        this.currentEditItem = dept;
        this.showModal('Edit Department', formHTML, 'department', true);
    }

    deleteDepartment(id) {
        if (confirm('Are you sure you want to delete this department?')) {
            this.dataManager.data.departments = this.dataManager.data.departments.filter(d => d.id !== id);
            this.dataManager.saveData();
            this.refreshDepartments();
            this.refreshDashboard();
            showToast('Department deleted successfully', 'success');
        }
    }

    // ====================================
    // SETTINGS
    // ====================================

    refreshSettings() {
        document.getElementById('universityName').value = this.dataManager.data.university.name;
        document.getElementById('universityAddress').value = this.dataManager.data.university.address;
    }

    saveUniversityDetails(e) {
        e.preventDefault();
        this.dataManager.data.university.name = document.getElementById('universityName').value;
        this.dataManager.data.university.address = document.getElementById('universityAddress').value;
        this.dataManager.saveData();
        this.refreshDashboard();
        showToast('University details saved successfully', 'success');
    }

    // ====================================
    // MODAL & FORMS
    // ====================================

    showModal(title, formHTML, type, isEdit = false) {
        document.getElementById('modalTitle').textContent = title;
        document.getElementById('formFields').innerHTML = formHTML;
        document.getElementById('modal').classList.add('active');
        this.currentEditType = type;
        
        if (!isEdit) {
            this.currentEditItem = null;
        }
    }

    closeModal() {
        document.getElementById('modal').classList.remove('active');
        document.getElementById('modalForm').reset();
        this.currentEditItem = null;
        this.currentEditType = null;
    }

    handleFormSubmit(e) {
        e.preventDefault();
        
        switch(this.currentEditType) {
            case 'student':
                this.saveStudent();
                break;
            case 'faculty':
                this.saveFaculty();
                break;
            case 'course':
                this.saveCourse();
                break;
            case 'department':
                this.saveDepartment();
                break;
        }
        
        this.closeModal();
    }

    saveStudent() {
        const id = document.getElementById('studentId').value;
        const name = document.getElementById('studentName').value;
        const age = parseInt(document.getElementById('studentAge').value);
        const gender = document.getElementById('studentGender').value;
        const department = document.getElementById('studentDepartment').value;
        
        const courseCheckboxes = document.querySelectorAll('input[name="courses"]:checked');
        const courses = Array.from(courseCheckboxes).map(cb => cb.value);
        
        const grades = {};
        courses.forEach(courseId => {
            const gradeInput = document.querySelector(`input[name="grade_${courseId}"]`);
            if (gradeInput && gradeInput.value) {
                grades[courseId] = parseFloat(gradeInput.value);
            }
        });

        if (this.currentEditItem) {
            // Update existing
            this.currentEditItem.name = name;
            this.currentEditItem.age = age;
            this.currentEditItem.gender = gender;
            this.currentEditItem.department = department;
            this.currentEditItem.courses = courses;
            this.currentEditItem.grades = grades;
        } else {
            // Add new
            const student = new Student(id, name, age, gender, department, courses, grades);
            this.dataManager.data.students.push(student);
        }
        
        // Update courses
        this.dataManager.data.courses.forEach(course => {
            if (courses.includes(course.id) && !course.enrolledStudents.includes(id)) {
                course.enrolledStudents.push(id);
            } else if (!courses.includes(course.id) && course.enrolledStudents.includes(id)) {
                course.enrolledStudents = course.enrolledStudents.filter(sid => sid !== id);
            }
        });
        
        this.dataManager.saveData();
        this.refreshStudents();
        this.refreshDashboard();
        showToast(`Student ${this.currentEditItem ? 'updated' : 'added'} successfully`, 'success');
    }

    saveFaculty() {
        const id = document.getElementById('facultyId').value;
        const name = document.getElementById('facultyName').value;
        const department = document.getElementById('facultyDepartment').value;

        if (this.currentEditItem) {
            // Update existing
            this.currentEditItem.name = name;
            this.currentEditItem.department = department;
        } else {
            // Add new
            const faculty = new Faculty(id, name, department);
            this.dataManager.data.faculty.push(faculty);
        }
        
        this.dataManager.saveData();
        this.refreshFaculty();
        this.refreshDashboard();
        showToast(`Faculty ${this.currentEditItem ? 'updated' : 'added'} successfully`, 'success');
    }

    saveCourse() {
        const id = document.getElementById('courseId').value;
        const name = document.getElementById('courseName').value;
        const creditHours = parseInt(document.getElementById('creditHours').value);
        const assignedFaculty = document.getElementById('assignedFaculty').value || null;

        if (this.currentEditItem) {
            // Update existing
            const oldFacultyId = this.currentEditItem.assignedFaculty;
            this.currentEditItem.name = name;
            this.currentEditItem.creditHours = creditHours;
            this.currentEditItem.assignedFaculty = assignedFaculty;
            
            // Update faculty coursesTaught
            if (oldFacultyId) {
                const oldFaculty = this.dataManager.data.faculty.find(f => f.id === oldFacultyId);
                if (oldFaculty) {
                    oldFaculty.coursesTaught = oldFaculty.coursesTaught.filter(cid => cid !== id);
                }
            }
            if (assignedFaculty) {
                const newFaculty = this.dataManager.data.faculty.find(f => f.id === assignedFaculty);
                if (newFaculty && !newFaculty.coursesTaught.includes(id)) {
                    newFaculty.coursesTaught.push(id);
                }
            }
        } else {
            // Add new
            const course = new Course(id, name, creditHours, assignedFaculty);
            this.dataManager.data.courses.push(course);
            
            // Update faculty
            if (assignedFaculty) {
                const faculty = this.dataManager.data.faculty.find(f => f.id === assignedFaculty);
                if (faculty) {
                    faculty.coursesTaught.push(id);
                }
            }
        }
        
        this.dataManager.saveData();
        this.refreshCourses();
        this.refreshDashboard();
        showToast(`Course ${this.currentEditItem ? 'updated' : 'added'} successfully`, 'success');
    }

    saveDepartment() {
        const id = document.getElementById('deptId').value;
        const name = document.getElementById('deptName').value;
        const head = document.getElementById('deptHead').value;

        if (this.currentEditItem) {
            // Update existing
            this.currentEditItem.name = name;
            this.currentEditItem.headOfDepartment = head;
        } else {
            // Add new
            const dept = new Department(id, name, head);
            this.dataManager.data.departments.push(dept);
        }
        
        this.dataManager.saveData();
        this.refreshDepartments();
        this.refreshDashboard();
        showToast(`Department ${this.currentEditItem ? 'updated' : 'added'} successfully`, 'success');
    }

    // ====================================
    // SEARCH
    // ====================================

    searchTable(type, query) {
        const table = document.getElementById(`${type}Table`);
        const tbody = table.querySelector('tbody');
        const rows = tbody.querySelectorAll('tr');
        
        query = query.toLowerCase();
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(query) ? '' : 'none';
        });
    }

    // ====================================
    // REFRESH ALL
    // ====================================

    refreshAll() {
        this.refreshDashboard();
        this.refreshStudents();
        this.refreshFaculty();
        this.refreshCourses();
        this.refreshDepartments();
        this.refreshSettings();
    }
}

// ====================================
// TOAST NOTIFICATIONS
// ====================================

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ====================================
// APPLICATION INITIALIZATION
// ====================================

class App {
    constructor() {
        this.dataManager = new DataManager();
        this.ui = new UIManager(this.dataManager);
    }

    async init() {
        await this.dataManager.loadData();
        this.ui.init();
    }

    refreshAll() {
        this.ui.refreshAll();
    }
}

// Initialize the application
const app = new App();

// Wait for DOM to be ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => app.init());
} else {
    app.init();
}
