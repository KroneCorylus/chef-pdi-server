CREATE TABLE IF NOT EXISTS job_execution (
   job_name TEXT,
   pid INTEGER,
   stdout TEXT,
   stderr TEXT,
   return_code INTEGER,
   init_date TEXT,
   end_date TEXT,
   id_sequence_execution INTEGER,
   parameters TEXT
);

CREATE TABLE IF NOT EXISTS sequence_execution (
   sequence_name TEXT,
   init_date TEXT,
   end_date TEXT, 
   parameters TEXT
) 
