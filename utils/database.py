import psycopg2


class DatabaseUtils:
    def __init__(self, db_config):
        self.db_config = db_config

        try:
            self.connection = psycopg2.connect(
                host=db_config["host"],
                port=db_config["port"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"],
            )

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None
            

    def schema_details(self,schema_name):

        connection=self.connection
        cursor=connection.cursor()

        schema_context=""

        if cursor is None:
            print("Database connection is not established.")
            return None

        try:
            cursor.execute("SELECT table_name from information_schema.tables where table_schema = %s;", (schema_name,))

            tables = cursor.fetchall()
            # print(tables)

            for table in tables:
                table_name=table[0]
                # Now i need to get the columns of this table
                schema_context+=f"These are the complete information for the table {table_name} \n"

                cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s",(table_name,))
                columns=cursor.fetchall()
                schema_context+=f"Below is the column information \n"
                for col in columns:
                    column_name, data_type=col
                    schema_context+=f"{column_name} : {data_type}\n"

                #now need to get the sample information
                cursor.execute(f"SELECT * FROM {schema_name}.{table_name} LIMIT 5;")
                sample_data=cursor.fetchall()
                # print(sample_data)
                schema_context+=f"Below is the sample data from the table \n"
                for row in sample_data:
                    schema_context=f"{schema_context}  {row},\n"

                schema_context+="\n\n\n\n"

            return schema_context


        except Exception as e:
            print(f"Error retrieving schema details: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def run_sql_query(self,query):
        # print(self.connection)
        connection=self.connection
        cursor=connection.cursor()
        try:
            
            cursor.execute(query)
            result=cursor.fetchall()
            return str(result)   

        except Exception as e:
            print(f"Error retrieving schema details: {e}")
            return None
                
        finally:
            
            if cursor:
                cursor.close()
            if connection:
                connection.close()

         



        

# obj = DatabaseUtils(
#     {
#         "host": "localhost",
#         "port": 5432,
#         "user": "postgres",
#         "password": "postgres",
#         "database": "postgres",
#     }
# )
# res=obj.schema_details('public')



# with open("schema_details.txt", "w") as f:
#     f.write(res)
