### Record Databse Model ###
from application import db
from datetime import datetime
from sqlalchemy import exc


class Record (db.Model):


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    created_on = db.Column(db.String(120))
    description = db.Column(db.String(1024))
    tag = db.Column(db.String(64))
    timeline = db.Column(db.Integer)
    content_type = db.Column(db.String(64))
    status = db.Column(db.String(64))

    def __init__ (self, name = None, description = None, tag = "unindentified", timeline = 0, content_type = "image", status = "Unverified"):
        self.name = name
        self.status = status
        self.description = description
        self.content_type = content_type
        self.tag = tag
        self.timeline = timeline
        self.created_on = datetime.strftime (datetime.now(), '%m/%d/%y %H:%M:%S')


    def __repr__ (self):
        return f"Record {self.id}, Source : {self.source}, Date : {self.created_on}"


    def __call__ (self):
        return {
            'id' : self.id,
            'name' : self.name,
            'content-type' : self.content_type,
            'description' : self.description,
            'tag' : self.tag,
            'timeline': self.timeline,
            'status' : self.status,
            'created on' : self.created_on
        }


    def add_desc_only(self) -> int:
        db.session.add(self)
        db.session.commit()
        return self.id


    @classmethod
    def add_file (cls, _id, **kwargs):
        record = cls.find_record_by_id(_id)
        if not record:
            return -1
        record.name = kwargs['name']
        record.content_type = kwargs['content-type']
        db.session.commit()

    
    def add_record (self):
        db.session.add (self)
        db.session.commit()
    

    def remove_record (self, _id):
        record = self.find_record_by_id(_id)
        if record:
            db.session.remove (record)
            db.session.commit()
            return 1
        return -1
        

    @classmethod
    def find_record_by_name (cls, _name):
        return cls.query.filter_by(name = _name).first()


    @classmethod
    def find_record_by_id (cls, _id):
        return cls.query.filter_by(id=_id).first()
    

    @classmethod
    def get_records (cls, id = None):
        if id is None:
            return [ record() for record in cls.query.all() ]


    @classmethod
    def get_records_by_type (cls, _type):
        return [ record() for record in cls.query.filter_by(content_type = _type) ]

