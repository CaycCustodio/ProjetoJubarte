from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finance_engine.database.models import Base

# Usaremos SQLite local para facilidade de teste do usuário
DATABASE_URL = "sqlite:///./finance_platform.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Cria as tabelas no banco de dados se não existirem."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Providencia uma sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
