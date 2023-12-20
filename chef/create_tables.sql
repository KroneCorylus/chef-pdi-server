CREATE TABLE IF NOT EXISTS job_execution (
   job_name TEXT,
   pid INTEGER,
   stdout TEXT,
   stderr TEXT,
   return_code INTEGER,
   init_date TEXT,
   end_date TEXT,
   id_secuence_execution INTEGER
);

CREATE TABLE IF NOT EXISTS secuence_execution (
   secuence_name TEXT,
   init_date TEXT,
   end_date TEXT
) 
