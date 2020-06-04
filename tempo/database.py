from mysql import connector

SELECTALL = 'SELECT * FROM users;'

connection = connector.connect(
    user="kotano@tempotm",
    password='@Uppjer6@EvVL2G',
    host="tempotm.mysql.database.azure.com",
    port=3306,
    database='tempo',
    # ssl_ca={ca-cert filename}, ssl_verify_cert=true)
)


cur = connection.cursor()

cur.execute(SELECTALL)
result = cur.fetchall()

for x in result:
    print(x)

# connection.commit()

connection.close()
