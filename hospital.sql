-- IMPORT  CSV FILE TO DATABASE
.mode csv
.import /Users/vytran/Downloads/SQL_final_project/DataFiles/doctors.csv DOCTORS
.import /Users/vytran/Downloads/SQL_final_project/DataFiles/patients.csv PATIENTS
.import /Users/vytran/Downloads/SQL_final_project/DataFiles/nurses.csv NURSES
.import /Users/vytran/Downloads/SQL_final_project/DataFiles/p_assignment.csv P_ASSIGNMENT
.import /Users/vytran/Downloads/SQL_final_project/DataFiles/n_assists.csv N_ASSISTS
.import /Users/vytran/Downloads/SQL_final_project/DataFiles/tests.csv TESTS
.import /Users/vytran/Downloads/SQL_final_project/DataFiles/instruments.csv INSTRUMENTS

-- FORCE ALL IDS TO BE INTEGERS
UPDATE DOCTORS SET D_ID = CAST(D_ID AS INTEGER);
UPDATE PATIENTS SET P_ID = CAST(P_ID AS INTEGER);
UPDATE NURSES SET N_ID = CAST(N_ID AS INTEGER);
UPDATE P_ASSIGNMENT SET P_ID = CAST(P_ID AS INTEGER);
UPDATE P_ASSIGNMENT SET D_ID = CAST(D_ID AS INTEGER);
UPDATE N_ASSISTS SET N_ID = CAST(N_ID AS INTEGER); 
UPDATE N_ASSISTS SET D_ID = CAST(D_ID AS INTEGER);
UPDATE TESTS SET T_ID = CAST(T_ID AS INTEGER);
UPDATE TESTS SET P_ID = CAST(P_ID AS INTEGER);
UPDATE TESTS SET D_ID = CAST(D_ID AS INTEGER);
UPDATE TESTS SET I_ID = CAST(I_ID AS INTEGER);
UPDATE INSTRUMENTS SET I_ID = CAST(I_ID AS INTEGER);

-- query 1
SELECT char(10);
SELECT "=== 1) List all the doctors that patient RICHARD MILLER is visitng ===";

SELECT DOCTORS.D_NAME
FROM DOCTORS
JOIN P_ASSIGNMENT ON DOCTORS.D_ID = P_ASSIGNMENT.D_ID
JOIN PATIENTS ON PATIENTS.P_ID = P_ASSIGNMENT.P_ID
WHERE PATIENTS.P_NAME = 'RICHARD MILLER';

-- query 2
SELECT char(10);
SELECT "=== 2) Find all the test results of cancer patients. (Note: There may be different type of cancer) ===";

SELECT P.P_NAME, T.*
FROM TESTS T
JOIN PATIENTS P ON T.P_ID = P.P_ID
WHERE P.P_DISEASE LIKE '%cancer%';

SELECT char(10);
SELECT "=== 3) List all the instruments produced by a manufacturer whose name starts with 'S' ===";

SELECT *
FROM INSTRUMENTS
WHERE I_MANUFACTURER LIKE 'S%'; 

-- query 4
SELECT char(10);
SELECT "=== 4) Find the most experienced doctor in the hospital. ===";
SELECT D_NAME, MAX(CAST(D_YEARS_OF_EXPERIENCE AS INTEGER)) AS exp FROM DOCTORS;

-- query 5
SELECT char(10);
SELECT "=== 5) List all the patients of doctor JAMES SMITH who live in the same street and same city as him. ===";

SELECT P.*
FROM PATIENTS P
JOIN P_ASSIGNMENT PA ON P.P_ID = PA.P_ID
JOIN DOCTORS D ON PA.D_ID = D.D_ID
WHERE D.D_NAME = 'JAMES SMITH' AND P.P_STREET = D.D_STREET AND P.P_CITY = D.D_CITY;

-- query 6
SELECT char(10);
SELECT "=== 6) Find the nurses who assist at least two doctors. Display nurse name and the number of doctors he/she is assisting ===";

SELECT N.N_NAME, COUNT(DISTINCT NA.D_ID) AS Doctor_Count
FROM NURSES N
JOIN N_ASSISTS NA ON N.N_ID = NA.N_ID
GROUP BY N.N_NAME
HAVING COUNT(DISTINCT NA.D_ID) >= 2;

-- query 7
SELECT char(10);
SELECT "=== 7) List the doctors and the number of nurses they have in descending order of their number. ===";

SELECT D.D_NAME, COUNT(NA.N_ID) AS Nurse_Count
FROM DOCTORS D
LEFT JOIN N_ASSISTS NA ON D.D_ID = NA.D_ID
GROUP BY D.D_NAME
ORDER BY Nurse_Count DESC;

-- query 8
SELECT char(10);
SELECT "=== 8) Find all the nurses who are not assigned to any doctors ===";

SELECT N.*
FROM NURSES N
LEFT JOIN N_ASSISTS NA ON N.N_ID = NA.N_ID
WHERE NA.D_ID IS NULL;

-- query 9
SELECT char(10);
SELECT "=== 9) Increment years of experience of all the female doctors by 5 ===";

UPDATE DOCTORS
SET D_YEARS_OF_EXPERIENCE = CAST(D_YEARS_OF_EXPERIENCE AS INTEGER) + 5
WHERE D_GENDER = 'f';

-- print out updated D_YEARS_OF_EXPERIENCE values for female doctors
SELECT D_NAME, D_YEARS_OF_EXPERIENCE 
FROM DOCTORS 
WHERE D_GENDER = 'f';

-- query 10
SELECT char(10);
SELECT "=== 10) Delete all the tests whose result is negative. ===";

DELETE FROM TESTS
WHERE T_RESULT = 'Negative';

-- Dump into hospitaldb.sql
.output hospitaldb.sql
.dump
