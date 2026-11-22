# SS Solar Solutions — Flask Solar Business Website

A complete Flask + SQLite starter for SS Solar Solutions, using the supplied SS Solar logo/branding.

## Features

### Customer Panel
- Premium home page
- Solar services
- Government schemes/subsidy information
- Solar loan + EMI calculator
- Solar system calculator
- Projects showcase
- Individual project details
- Image gallery with filters and lightbox
- About Us
- Offices
- Enquiry form
- Direct call / WhatsApp / Instagram / email

### Admin Panel
- Secure admin login
- Dashboard KPIs
- Monthly business growth chart
- Business revenue / enquiry / project / installed-KW records
- Customer database
- All enquiries + status workflow
- Add/delete projects
- Featured projects on home page
- Add/delete services
- Add/delete government schemes
- Add/delete offices
- Add/delete gallery images
- Loan information management
- Image upload support

## Run locally

1. Open this folder in VS Code.
2. Create a virtual environment:
   `python -m venv venv`
3. Activate:
   Windows:
   `venv\Scripts\activate`
4. Install:
   `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`.
6. Run:
   `python app.py`
7. Open:
   `http://127.0.0.1:5000`

## Demo admin


Change these values in `.env` before deploying.

## Important production notes

- Replace the secret key.
- Change the admin password.
- Keep government subsidy figures aligned with current official notifications.
- The loan calculator is an indicative calculator, not a lender approval or guaranteed offer.
- Add your real project/gallery photos through Admin Panel.
