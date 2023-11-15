from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import pandas as pd

# Define the database and Base
engine = create_engine('sqlite:///hospital.db')
Base = declarative_base()

# Define the classes/tables
class Nurse(Base):
    __tablename__ = 'nurses'
    N_ID = Column(Integer, primary_key=True)
    N_NAME = Column(String)
    N_SPECIALIZATION = Column(String)
    N_SHIFT = Column(String)
    N_STREET = Column(String)
    N_CITY = Column(String)

class NAssists(Base):
    __tablename__ = 'n_assists'
    id = Column(Integer, primary_key=True)
    N_ID = Column(Integer, ForeignKey('nurses.N_ID'))
    D_ID = Column(Integer, ForeignKey('doctors.D_ID'))
    nurse = relationship("Nurse")
    doctor = relationship("Doctor")

class Test(Base):
    __tablename__ = 'tests'
    T_ID = Column(Integer, primary_key=True)
    T_NAME = Column(String)
    P_ID = Column(Integer, ForeignKey('patients.P_ID'))
    D_ID = Column(Integer, ForeignKey('doctors.D_ID'))
    I_ID = Column(Integer, ForeignKey('instruments.I_ID'))
    T_DATE = Column(DateTime)
    T_RESULT = Column(String)

class Instrument(Base):
    __tablename__ = 'instruments'
    I_ID = Column(Integer, primary_key=True)
    I_NAME = Column(String)
    I_MANUFACTURER = Column(String)

class Doctor(Base):
    __tablename__ = 'doctors'
    D_ID = Column(Integer, primary_key=True)
    D_NAME = Column(String)
    D_GENDER = Column(String)
    D_AGE = Column(Integer)
    D_SPECIALIZATION = Column(String)
    D_YEARS_OF_EXPERIENCE = Column(Integer)
    D_CONTACT = Column(String)
    D_STREET = Column(String)
    D_CITY = Column(String)

# PATIENTS table
class Patient(Base):
    __tablename__ = 'patients'
    P_ID = Column(Integer, primary_key=True)
    P_NAME = Column(String)
    P_GENDER = Column(String)
    P_AGE = Column(Integer)
    P_DISEASE = Column(String)
    P_CONTACT = Column(String)
    P_STREET = Column(String)
    P_CITY = Column(String)

# P_ASSIGNMENT table
class PAssignment(Base):
    __tablename__ = 'p_assignment'
    id = Column(Integer, primary_key=True)
    P_ID = Column(Integer, ForeignKey('patients.P_ID'))
    D_ID = Column(Integer, ForeignKey('doctors.D_ID'))
    patient = relationship("Patient")
    doctor = relationship("Doctor")

# Create the tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Function to import CSV files into the database
def import_csv_to_table(csv_path, table_class, date_columns=None):
    df = pd.read_csv(csv_path)

    # Convert date columns
    if date_columns:
        for date_column in date_columns:
            df[date_column] = pd.to_datetime(df[date_column], format='%m/%d/%Y', errors='coerce')

    df.to_sql(table_class.__tablename__, engine, if_exists='replace', index=False)


# Import CSV data
import_csv_to_table('DataFiles/doctors.csv', Doctor)
import_csv_to_table('DataFiles/patients.csv', Patient)
import_csv_to_table('DataFiles/nurses.csv', Nurse)
import_csv_to_table('DataFiles/tests.csv', Test, date_columns=['T_DATE'])
import_csv_to_table('DataFiles/instruments.csv', Instrument)
import_csv_to_table('DataFiles/n_assists.csv', NAssists)
import_csv_to_table('DataFiles/p_assignment.csv', PAssignment)

# Example queries and operations
from sqlalchemy.orm import aliased

print('\nQuery 1: List all the doctors that patient RICHARD MILLER is visiting')
richard_doctors = session.query(Doctor.D_NAME).\
    join(PAssignment, Doctor.D_ID == PAssignment.D_ID).\
    join(Patient, Patient.P_ID == PAssignment.P_ID).\
    filter(Patient.P_NAME == 'RICHARD MILLER').all()
for doctor in richard_doctors:
    print(doctor.D_NAME)

print('\nQuery 2: Find all the test results of cancer patients')
cancer_tests = session.query(Patient.P_NAME, Test).\
    join(Test, Patient.P_ID == Test.P_ID).\
    filter(Patient.P_DISEASE.like('%cancer%')).all()
for patient_name, test in cancer_tests:
    print(patient_name, test.T_ID, test.T_NAME, test.T_DATE, test.T_RESULT)

print('\nQuery 3: List all the instruments produced by a manufacturer whose name starts with "S"')
s_instruments = session.query(Instrument).\
    filter(Instrument.I_MANUFACTURER.like('S%')).all()
for instrument in s_instruments:
    print(instrument.I_ID, instrument.I_NAME, instrument.I_MANUFACTURER)

print('\nQuery 4: Find the most experienced doctor in the hospital')
most_experienced = session.query(Doctor.D_NAME, func.max(Doctor.D_YEARS_OF_EXPERIENCE)).first()
print(most_experienced.D_NAME, most_experienced[1])


print('\nQuery 5: List all the patients of doctor JAMES SMITH who live in the same street and same city as him')
james_smith_patients = session.query(Patient).\
    join(PAssignment, Patient.P_ID == PAssignment.P_ID).\
    join(Doctor, Doctor.D_ID == PAssignment.D_ID).\
    filter(Doctor.D_NAME == 'JAMES SMITH', Patient.P_STREET == Doctor.D_STREET, Patient.P_CITY == Doctor.D_CITY).all()
for patient in james_smith_patients:
    print(patient.P_ID, patient.P_NAME)

print('\nQuery 6: Find the nurses who assist at least two doctors')
nurses_two_doctors = session.query(Nurse.N_NAME, func.count(NAssists.D_ID).label('Doctor_Count')).\
    join(NAssists, Nurse.N_ID == NAssists.N_ID).\
    group_by(Nurse.N_ID).\
    having(func.count(NAssists.D_ID) >= 2).all()
for nurse in nurses_two_doctors:
    print(nurse.N_NAME, nurse.Doctor_Count)

print('\nQuery 7: List the doctors and the number of nurses they have')
doctors_nurse_count = session.query(Doctor.D_NAME, func.count(NAssists.N_ID).label('Nurse_Count')).\
    outerjoin(NAssists, Doctor.D_ID == NAssists.D_ID).\
    group_by(Doctor.D_ID).\
    order_by(func.count(NAssists.N_ID).desc()).all()
for doctor in doctors_nurse_count:
    print(doctor.D_NAME, doctor.Nurse_Count)

print('\nQuery 8: Find all the nurses who are not assigned to any doctors')
unassigned_nurses = session.query(Nurse).\
    outerjoin(NAssists, Nurse.N_ID == NAssists.N_ID).\
    filter(NAssists.D_ID == None).all()
for nurse in unassigned_nurses:
    print(nurse.N_ID, nurse.N_NAME)

print('\nQuery 9: Increment years of experience of all the female doctors by 5')
session.query(Doctor).\
    filter(Doctor.D_GENDER == 'f').\
    update({Doctor.D_YEARS_OF_EXPERIENCE: Doctor.D_YEARS_OF_EXPERIENCE + 5}, synchronize_session='fetch')
session.commit()

# Print out updated D_YEARS_OF_EXPERIENCE values for female doctors
updated_female_doctors = session.query(Doctor.D_NAME, Doctor.D_YEARS_OF_EXPERIENCE).\
    filter(Doctor.D_GENDER == 'f').all()
for doctor in updated_female_doctors:
    print(doctor.D_NAME, doctor.D_YEARS_OF_EXPERIENCE)

print('\nQuery 10: Delete all the tests whose result is negative')
session.query(Test).filter(Test.T_RESULT == 'Negative').delete(synchronize_session='fetch')
session.commit()

# Close the session
session.close()
