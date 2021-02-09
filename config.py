from os import environ, path



class Config:

    SECRET_KEY = 'there is no secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_PATH = 'application/static'
    BEGINNING = "Feb 6 2021 12:00AM"
    MAX_SIZE = 16 * 1024 * 1024 # 16 MB
    BASE_DIR = 'application/static'
    IMAGE_FOLDER = 'images'
    VIDEO_FOLDER = 'videos'
