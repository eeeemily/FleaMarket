#General Description
Our project is a UR FleaMarket, i.e. a website where students can put information about products they want to sell.
It consists of an authentication part, which requires a user to create an account. We keep users’ passwords hashed using SHA256 so even if our database is hacked into, it is impossible to retrieve user’s passwords.
Other than that, we have two possible scenarios in which a user can be found:
-Logged out: In this scenario, they can only scroll through the webpage and look at posts by other users without seeing the seller’s name and contact information.
-Logged in: In this scenario, they can see the seller’s information and can further contact them on their own.a


#CRUD Functionality
Our database consists of two tables; User and Product that are related with a one-to-many relationship, i.e. one user can have multiple products posted.
The user creates an account by putting their information which we store in the database. 
Under the section “Profile”, the user can add items to sell by inputting a title, description, price and a picture of their product. All of this can be updated further, and can be deleted by the seller. Thus, we have a fully functional CRUD application.

Project done by:
-Kushal Gautam
-Anisha Bhattacharya
-Minghui Zheng
-Nikola Danevski
