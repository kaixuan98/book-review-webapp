import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError


engine = create_engine(os.getenv("DATABASE_URL")) 
db = scoped_session(sessionmaker(bind=engine))

def add_author():
    f = open('books.csv')
    reader = csv.reader(f)
    next(reader)
    # here is adding unqiue author and assuming that author name is unique
    for isbn , title ,author , year in reader: 
        if db.execute("SELECT author_name FROM \"author\" WHERE author_name = :author " , 
                        {"author" : author}).rowcount > 0 : 
            next(reader ,'-1')
            print(f"-------------------------->already added {author}")
        else: 
            db.execute("INSERT INTO \"author\" (author_name) VALUES (:author) " , 
            {"author": author})
            print(f"added {author}")
    print("finished author")
    db.commit()
# here is adding unqiue year into the year table and 
def add_year():
    f = open('books.csv')
    reader = csv.reader(f)
    next(reader)
    for isbn , title ,author , year in reader: 
        year_int = int(year , base=10)
        if db.execute("SELECT year_value FROM \"year\" WHERE year_value = :year" , 
                        {"year" : year}).rowcount > 0: 
            next(reader , '-1')
            print(f"-------------------------->already added {year_int}")
        else:
            db.execute("INSERT INTO \"year\" (year_value) VALUES (:year) " , 
                            {"year":year_int})
            print(f"added {year_int}")
            
    print("finished year")
    db.commit()


def add_books():
    count = 0 ; 
    f = open('books.csv')
    reader = csv.reader(f)
    next(reader)
    
    for isbn , title , author , year in reader: 
        author_count = db.execute("SELECT id FROM \"author\" WHERE author_name = :author" , 
                                    {"author" : author}).rowcount
        year_int = int(year , base=10)
        year_count = db.execute("SELECT id FROM \"year\" WHERE year_value = :year" , 
                                {"year" : year_int}).rowcount
        if author_count == 1 and year_count == 1 : 
            author_id = db.execute("SELECT * FROM \"author\" WHERE author_name = :author" , 
                                        {"author" : author}).fetchone()
            year_id = db.execute("SELECT * FROM \"year\" WHERE year_value = :year" , 
                                        {"year" : year_int}).fetchone()
            db.execute("INSERT INTO \"books\" (isbn , title , author_id , year_id ) VALUES (:isbn , :title , :author_id , :year_id)" , 
                   {"isbn" : isbn , "title": title , "author_id" : author_id.id, "year_id" : year_id.id })
            print(f"added {isbn} , {title} , {author_id.id} , {year_id.id}")
        else:
            count += 1 ; 
            print(f"did not add ------------------------------ {isbn} , {title} , {author_id.id} , {year_id.id}")
    
    print(f"count : {count}")

        
        


if __name__ == "__main__":
    #add_author()
    #add_year()
    add_books()
    



    




    