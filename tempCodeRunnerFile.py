app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI", "sqlite:///posts.db")
