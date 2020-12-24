# Book Review webapp  ( Coffee & Books)

--- Currently on going Project ---

Book review webapp that build with Flask and HTML / CSS(Bootstrap) 

The webapp contain the following feature: 

<ol>
  <li><strong>Done</strong>The webapp contain a register , login and logout feature</li>
  <li><strong>Done but need refinement</strong>User able to search for books </li>
  <li><strong>Working</strong>user able to add the books to its own bookshelf ( session)  </li>
</ol>


<h3>Further Explaination of features </h3>
<ol>
  <li>
    User Registration , Login and Logout 
  </li>
  <p> The user that registered are stored into a database by using Flask-SQLAlchemy </br> The user able to login and logout the webpage. If the user already created an account , will not be able to register again. If user login into his/her account, the user will be stored in a session. User will keep login until they closed the browser or logout </br> The user login and logout is handle with flask (session)  </p>
  
   <li>
    Search Features
  </li>
  <p>Used Google Books APIT to search for books</p>
 </ol>
 
 ---
 
 <h3>Extra material in the project.  </h3>
 -Import.py ( Still working on the importcsv branch ) 
    </br> The import.py is the python script that used to import books.csv into the database 
    </br> The data been seperated into different individual tables to improve data consistency. 



