from app.db.session import engine
from app.models.db_models import Base, Source


def init_db() -> None:
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def seed_sources() -> None:
    """Insert default feedback sources if they don't exist."""
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        defaults = [
            Source(name="app_review", type="review"),
            Source(name="support_ticket", type="ticket"),
            Source(name="email", type="email"),
            Source(name="crm", type="crm"),
            Source(name="manual", type="manual"),
        ]
        for src in defaults:
            if not db.query(Source).filter_by(name=src.name).first():
                db.add(src)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_sources()
    print("Database initialised and seeded.")
