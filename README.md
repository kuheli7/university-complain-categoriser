# CHRIST University Complaint Intelligence System

A rule-based intelligent complaint categorization system for CHRIST University students. Complaints are automatically classified into categories and assigned a priority level using keyword matching — no machine learning required.

## Demo Link: https://university-complain-categoriser.streamlit.app/

---

## Features

### Single Complaint Analysis
- Type any complaint and get instant categorization
- Displays the most recent result with category and priority
- Full session history shown below — most recent first

### Bulk CSV Processing
- Upload a CSV with a `Complaint_Text` column
- Processes all entries at once
- Key metrics: total complaints, top category, high priority count, success rate
- Auto-generated insights after processing
- Filter the results table by category and/or priority
- Download the processed CSV

### Analytics Dashboard
- Pie chart and bar chart for category distribution
- Category and priority breakdown in text form
- Priority vs Category heatmap
- High priority complaints highlighted separately

### Smart Priority Detection
Complaints are automatically assigned a priority based on keywords in the text:
- **High** — urgent, emergency, broken, not working, critical, asap, severe
- **Medium** — issue, problem, need, important, please, required, soon
- **Low** — everything else (default)

---

## Categories

| Category | Keywords |
|---|---|
| Academic | exam, marks, syllabus, assignment, faculty, professor, grade, course |
| Hostel | wifi, room, mess, food, warden, water, accommodation, internet |
| Infrastructure | library, lab, classroom, projector, computer, equipment, furniture, ac |
| Administration | fees, id card, scholarship, certificate, documents, payment, registration |

If no keyword matches, the complaint is classified as **Other**.

---

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## CSV Format

```csv
Complaint_Text
My exam marks are not updated
Hostel wifi is not working urgently
Library computers are slow
Fees receipt not generated
```

---

## Tech Stack

- **Streamlit** — web interface
- **Pandas** — data handling
- **Plotly** — interactive charts
- **Python** — rule-based NLP logic

---

## Project Structure

```
Cia 3/
├── app.py                    # Streamlit application
├── sample_complaints.csv     # Sample data for testing
├── requirements.txt          # Python dependencies
├── logo.png                  # Sidebar logo
└── README.md                 # Documentation
```

---

## Future Enhancements

- Multi-language support for regional complaints
- Email or SMS notifications for high priority cases
- Admin panel for managing and updating keywords
- Database integration for persistent complaint records
- Historical trend analysis across semesters

---

**CHRIST University | MCA519A-3 Advanced Python Programming | 2026**
