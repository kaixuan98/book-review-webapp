import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError


engine = create_engine(os.getenv("DATABASE_URL")) 
db = scoped_session(sessionmaker(bind=engine))

def main():
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
    # here is adding unqiue year into the year table and 
    for isbn , title ,author , year in reader: 
        if db.execute("SELECT year_value FROM \"year\" WHERE year_value = :year" , 
                        {"year" : year}).rowcount > 0: 
            next(reader)
        else:
            year_int = int(year , base=10)
            db.execute("INSERT INTO \"year\" (year_values) VALUES (:year) " , 
                            {"year":year_int})
            print(f"added {year_int}")
            
    print("finished")
    
        #year_int = int(year , base=10)
        

    #     db.execute("INSERT INTO \"year\" (year_value) VALUES (:year)", 
    #         {"year": year_int })
    #     db.execute("INSERT INTO \"books\" (isbn , title) VALUES (:isbn , :title)" , 
    #         {"isbn": isbn , "title" : title })
    #     db.commit()

    # author_ids = db.execute("SELECT * FROM \"author\" ").fetchall()

    # for author in reader: 
    #     for author_id , author_name in author_ids: 
    #         if author == author_name:
    #             db.execute("INSERT INTO \"books\" (author_id) VALUES(:author_id)", 
    #                         {"author_id": author_id})
    #             db.commit()

    # year_list = db.execute("SELECT * FROM \"year\" ").fetchall()

    # for year in reader: 
    #     for year_id , year_value in year_list:
    #         if year == year_value:
    #             db.execute("INSERT INTO \"books\" (year_id) VALUES (:year_id)" , 
    #                         {"year_id" : year_id})
    #             db.commit()

if __name__ == "__main__":
    main()



    




    