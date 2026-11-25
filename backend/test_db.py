from app import app
from extensions import db

try:
    with app.app_context():
        connection = db.engine.connect()

        print("✅ Database connection successful!")

        connection.close()

except Exception as e:
    print("❌ Database connection failed!")
    print(e)