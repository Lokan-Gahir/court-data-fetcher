from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///court_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CaseQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(100), nullable=False)
    case_number = db.Column(db.String(50), nullable=False)
    filing_year = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class CourtDataError(Exception):
    pass

class InvalidCaseError(CourtDataError):
    pass

class CourtWebsiteError(CourtDataError):
    pass

@app.errorhandler(HTTPException)
def handle_http_error(e):
    return render_template('error.html',
                         error_code=e.code,
                         error_title=e.name,
                         error_message=e.description), e.code

@app.errorhandler(CourtDataError)
def handle_court_error(e):
    return render_template('error.html',
                         error_code=400,
                         error_title="Case Data Error",
                         error_message=str(e)), 400

@app.errorhandler(Exception)
def handle_unexpected_error(e):
    app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    return render_template('error.html',
                         error_code=500,
                         error_title="System Error",
                         error_message="Our team has been notified. Please try later."), 500

def validate_input(case_type, case_number, filing_year):
    if not case_type:
        raise InvalidCaseError("Please select a case type")
    if not case_number.isalnum():
        raise InvalidCaseError("Case number can only contain letters and numbers")
    if not filing_year.isdigit() or len(filing_year) != 4:
        raise InvalidCaseError("Filing year must be a 4-digit number")
    return True

def get_mock_data(case_type, case_number, filing_year):
    case_types = {
        'CRIMINAL': {'judge': 'Hon. Justice Sharma', 'stage': 'Trial'},
        'CIVIL': {'judge': 'Hon. Justice Patel', 'stage': 'Evidence'},
        'FAMILY': {'judge': 'Hon. Justice Gupta', 'stage': 'Mediation'}
    }
    
    return {
        'case_number': f"{case_type}/{case_number}/{filing_year[-2:]}",
        'parties': [
            {'name': 'Petitioner: State of Delhi', 'role': 'Petitioner'},
            {'name': f'Respondent: Case {case_number}', 'role': 'Respondent'}
        ],
        'filing_date': f"{filing_year}-01-01",
        'next_hearing': f"{datetime.now().year}-12-31",
        'judge': case_types.get(case_type, {}).get('judge', 'Hon. Justice'),
        'stage': case_types.get(case_type, {}).get('stage', 'Hearing'),
        'documents': [
            {'name': 'Initial Filing', 'date': f"{filing_year}-01-15", 'url': '#'},
            {'name': 'Latest Order', 'date': f"{datetime.now().year}-01-01", 'url': '#'}
        ]
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    case_types = [
        ('CRIMINAL', 'Criminal Case'),
        ('CIVIL', 'Civil Case'),
        ('FAMILY', 'Family Case')
    ]
    
    if request.method == 'POST':
        try:
            case_type = request.form.get('case_type')
            case_number = request.form.get('case_number', '').strip()
            filing_year = request.form.get('filing_year', '').strip()
            
            validate_input(case_type, case_number, filing_year)
            
            if case_number == "ERROR500":
                raise Exception("Test error scenario")
                
            if case_number == "MAINTENANCE":
                raise CourtWebsiteError("Court website under maintenance until 5 PM")
            
            case_data = get_mock_data(case_type, case_number, filing_year)
            
            new_query = CaseQuery(
                case_type=case_type,
                case_number=case_number,
                filing_year=filing_year
            )
            db.session.add(new_query)
            db.session.commit()
            
            return render_template('results.html', 
                                case_data=case_data,
                                now=datetime.now())
            
        except InvalidCaseError as e:
            flash(str(e), 'danger')
        except CourtWebsiteError as e:
            flash(f"⚠️ {str(e)}", 'warning')
        except Exception as e:
            flash("⚡ An unexpected error occurred", 'danger')
            app.logger.error(f"Error in index: {str(e)}", exc_info=True)
        
        return redirect(url_for('index'))
    
    return render_template('index.html', case_types=case_types)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)