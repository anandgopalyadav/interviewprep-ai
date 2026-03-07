# from app.database import engine

# try:
#     connection = engine.connect()
#     print("✅ Database connected successfully!")
#     connection.close()
# except Exception as e:
#     print("❌ Error:", e)


from app.database import engine, Base
from app import models

# Create tables
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")
