from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .customer import Customer
from .enquiry import Enquiry
from .service import Service
from .project import Project
from .scheme import Scheme
from .office import Office
from .gallery import Gallery
from .loan import LoanSetting
from .business import BusinessRecord
