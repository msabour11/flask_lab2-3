class Config:
    @staticmethod
    def init_app():
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI= "sqlite:///project.sqlite"


class ProductionConfig(Config):
    DEBUG = False
    # postgresql://username:password@localhost:portnumber/dbname
    SQLALCHEMY_DATABASE_URI= "postgresql://postgres:123456@localhost:5432/flask2"



projectConfig={
    "dev": DevelopmentConfig,
    'prd': ProductionConfig
}
