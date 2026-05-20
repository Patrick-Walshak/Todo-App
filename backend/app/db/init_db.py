from app.db.session import Base, engine
import app.auth.models  # noqa
import app.todos.models  # noqa
import app.guest.models  # noqa

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
