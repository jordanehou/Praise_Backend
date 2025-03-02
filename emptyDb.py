from app.database import engine
from app.models import Base

# Supprime toutes les tables
Base.metadata.drop_all(bind=engine)

# Recrée toutes les tables
Base.metadata.create_all(bind=engine)

print("Base de données réinitialisée avec succès !")
