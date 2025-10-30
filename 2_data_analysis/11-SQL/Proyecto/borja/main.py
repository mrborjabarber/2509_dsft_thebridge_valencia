from utils import *

# Conexión a la base de datos
connection = psycopg2.connect(
        host=db_host,       
        database=db_name,        
        user=db_user,            
        password=db_password,        
        port=5432
        ) 

cursor = connection.cursor()

cursor.execute("SELECT version();")
print("Versión de PostgreSQL:", cursor.fetchone())

# Query -> Crear tablas BBDD
queries = [
    """
    CREATE TABLE IF NOT EXISTS Promocion (
        PromocionID SERIAL PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL,
        Fecha_inicio DATE DEFAULT CURRENT_DATE,
        Fecha_fin DATE DEFAULT CURRENT_DATE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Modalidad (
        ModalidadID SERIAL PRIMARY KEY,
        Dedicacion VARCHAR(50) NOT NULL,
        Tipo VARCHAR(50) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Campus (
        CampusID SERIAL PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL,
        Ciudad VARCHAR(50),
        Pais VARCHAR(50)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Aula (
        AulaID SERIAL PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL,
        CampusID INT NOT NULL,
        FOREIGN KEY (CampusID) REFERENCES Campus(CampusID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Bootcamp (
        BootcampID SERIAL PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL,
        CampusID INT NOT NULL,
        ModalidadID INT NOT NULL,
        AulaID INT NOT NULL,
        PromocionID INT NOT NULL,
        FOREIGN KEY (PromocionID) REFERENCES Promocion(PromocionID),
        FOREIGN KEY (ModalidadID) REFERENCES Modalidad(ModalidadID),
        FOREIGN KEY (AulaID) REFERENCES Aula(AulaID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Alumno (
        AlumnoID SERIAL PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL,
        Apellido VARCHAR(50) NOT NULL,
        Fecha_nac DATE DEFAULT CURRENT_DATE,
        Email VARCHAR(100),
        BootcampID INT NOT NULL,
        FOREIGN KEY (BootcampID) REFERENCES Bootcamp(BootcampID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Proyecto (
        ProyectoID SERIAL PRIMARY KEY,
        NombreProyecto VARCHAR(50) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Profesor (
        ProfesorID SERIAL PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL,
        Apellido VARCHAR(50) NOT NULL,
        Fecha_nac DATE DEFAULT CURRENT_DATE,
        Rol VARCHAR(50) NOT NULL,
        Email VARCHAR(100),
        CampusID INT NOT NULL,
        FOREIGN KEY (CampusID) REFERENCES Campus(CampusID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Calificacion (
        CalificacionID SERIAL PRIMARY KEY,
        Resultado VARCHAR(50) NOT NULL,
        ProyectoID INT NOT NULL,
        AlumnoID INT NOT NULL,
        FOREIGN KEY (ProyectoID) REFERENCES Proyecto(ProyectoID),
        FOREIGN KEY (AlumnoID) REFERENCES Alumno(AlumnoID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Profe_Curso (
        Profe_cursoID SERIAL PRIMARY KEY,
        ProfesorID INT NOT NULL,
        BootcampID INT NOT NULL,
        FOREIGN KEY (ProfesorID) REFERENCES Profesor(ProfesorID),
        FOREIGN KEY (BootcampID) REFERENCES Bootcamp(BootcampID)
    );
    """
]

# Ejecutar cada consulta individualmente
for query in queries:
    cursor.execute(query)
    
# Confirmar cambios
connection.commit()
print("Tablas creadas exitosamente.")


# Consultar y mostrar las tablas existentes en la base de datos
cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
""")
tablas = cursor.fetchall()
print("Tablas en la base de datos:")
for tabla in tablas:
    print(tabla[0])


# Crear un DataFrame leyendo el texto, usando ";" como separador
df = pd.read_csv('claustro_sep.csv', sep="," , index_col=0)

#Dataframe con los unicos campus de la BBDD
df_c = df['Campus'].unique()

# Iterar sobre los valores únicos y hacer el INSERT
for c in df_c:
    cursor.execute("INSERT INTO campus (nombre, ciudad, pais) VALUES (%s, %s, %s)", (c, c, 'España'))    #cursor.execute("INSERT INTO campus(nombre, ciudad, pais) VALUES ('recoletos', 'madrid', 'esp')")
    #cursor.execute (f"INSERT INTO campus(nombre, ciudad, pais) VALUES ({c}, {c}, 'Españaaa');")
    
# Hacer commit después del bucle
connection.commit()

# Inserción de  la tabla de alumnos
for index, row in df.iterrows():
    cursor.execute('''
    INSERT INTO profesor(nombre, apellido, fecha_nac, rol, email, campusid)
    VALUES (%s, %s, %s,%s, %s, %s)
    ''', (
        row['nombre'], 
        row['apellido'], 
        '1975-10-12',
        row['Rol'], 
        generar_email(row['nombre'], row['apellido']), 
        asignar_campus(row['Campus'])
    ))

connection.commit()

# Inserción de las distintas modalidades
cursor.execute("INSERT INTO modalidad (dedicacion, tipo) VALUES ('FT', 'Presencial')")
cursor.execute("INSERT INTO modalidad (dedicacion, tipo) VALUES ('FT', 'Online')")
cursor.execute("INSERT INTO modalidad (dedicacion, tipo) VALUES ('PT', 'Presencial')")
cursor.execute("INSERT INTO modalidad (dedicacion, tipo) VALUES ('PT', 'Online')")
cursor.execute("INSERT INTO modalidad (dedicacion, tipo) VALUES ('Hibrido', 'Presencial')")
cursor.execute("INSERT INTO modalidad (dedicacion, tipo) VALUES ('Hibrido', 'Online')")
    
connection.commit()


# Inserción de las promociones
cursor.execute("INSERT INTO promocion (nombre, fecha_inicio, fecha_fin) VALUES ('Febrero', '2024-02-12', '2024-05-31')")
cursor.execute("INSERT INTO promocion (nombre, fecha_inicio, fecha_fin) VALUES ('Septiembre', '2023-09-18', '2023-12-22')")
    
connection.commit()


# Inserción de la tabla de bootcamps
consultas = [6,3,3,4,5,5]

for i in consultas:
    cursor.execute('''
    INSERT INTO bootcamp(vertical, modalidadid, aulaid, promocionid)
    VALUES (%s, %s, %s, %s)
    ''', (
        random.choice(["DS","FT"]), 
        random.randint(1, 6),  
        random.randint(1, 6), 
        random.randint(2, 3)))
    

connection.commit()

# Inserción de la tabla de la tabla de alumnos
fechas = ['1985-03-17', '1987-11-05', '1992-04-28', '1995-09-12', '1988-02-29',
          '1998-07-15', '2001-12-31', '1990-06-20', '1989-01-01', '1994-08-18',
          '1997-05-23', '2003-02-14', '1986-10-31', '1991-03-07', '1999-11-25',
          '1993-08-04', '2002-05-19', '1985-12-25', '1996-04-01', '2000-09-09']

df_alu = pd.read_csv('clase_1_sep.csv', sep="," , index_col=0)
df_alu.reset_index(inplace=True, drop=True)

for index, row in df.iterrows():
    cursor.execute('''
    INSERT INTO alumno(nombre, apellido, fecha_nac,email, bootcampid)
    VALUES (%s, %s, %s,%s, %s)
    ''', (
        row['nombre'], 
        row['apellido'], 
        random.choice(fechas),
        row['Email'], 
        random.randint(1, 3)
    ))

connection.commit()

# Inserción de la tabla de calificaciones
for index, row in df_c.iterrows():
    cursor.execute('''
    INSERT INTO calificacion(resultado, proyectoid, alumnoid)
    VALUES (%s, %s, %s)
    ''', (
        random.choice(["Apto","No Apto"]), 
        row['Proyecto'],
        row['alumnoid']
        ))
    
connection.commit()

# Inserción de la tabla intermedia de profe_curso
cursor.execute("INSERT INTO profe_curso (profesorid, bootcampid) VALUES (8, 1)")
cursor.execute("INSERT INTO profe_curso (profesorid, bootcampid) VALUES (4, 1)")
cursor.execute("INSERT INTO profe_curso (profesorid, bootcampid) VALUES (1, 2)")
cursor.execute("INSERT INTO profe_curso (profesorid, bootcampid) VALUES (9, 2)")
cursor.execute("INSERT INTO profe_curso (profesorid, bootcampid) VALUES (3, 3)")
cursor.execute("INSERT INTO profe_curso (profesorid, bootcampid) VALUES (10, 3)")
    
connection.commit()

cursor.close()
connection.close()