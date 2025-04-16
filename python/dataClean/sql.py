import psycopg2

with open('C:/Users/jackk/Projects/horseData/postgresPassword.txt', 'r') as file:
    postgresPassword = file.read()

def executeSqlScript(sqlScriptAddress):
    conn = psycopg2.connect(
        host = "localhost",
        database = "horses",
        user = "karisch",
        password = postgresPassword,
        port = 5432
    )
    with open(sqlScriptAddress, 'r') as script:
        allCommands = [line.strip() for line in script.readlines()]
        with conn.cursor() as cur:
            for command in allCommands:
                cur.execute(command)

    conn.commit()
    conn.close()