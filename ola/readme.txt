Introduction

The main aim of the assignment was to build backend APIs for a taxi booking service like Ola/Uber.

I have used Django along with Postgres. I have made a single table for storing the information of customer and driver along with other tables for storing the information of driver like bank details, driver vehicle documents. Apart from these tables, one table for storing the booking history and rating for a ride.


API Documentation

There are mainly 6 APIs that I have made and details are as follows:

1. Register
In this API, both the customer and drivers intitally register themselves as a user account and on the type of the user, some other information of driver is stored.

The API takes general details in the body of a POST request like email, phone number, first name, gender, date of birth and password as required parameters and last name and isd code as optional parameters. Using these values, the details are initially verified if they are coming correctly or not and later if there is some user with same details is present or not. If yes, then APIs sends back a message that “User Already Registered” else the user is registered with different profile status for both type of users.

2. Driver Documents
In this API, driver documents like pan, licence, permit, vehicle documents are taken in POST request along with email in order to maintain the record of documents of driver.   

The API also checks if the user has successfully registered first and then trying to upload the documents. Based on the check above, the response of the API is success or failure.

3. Driver Bank Details
In this API, the bank details of the driver are stored to maintain a history of payments made to driver by the company. 

The API takes general details in the body of a POST request like email, account number, bank name, branch name, ifsc code, micr code, city, state, proof and proof type. Also, data validation is also using the for ifsc and micr code in order to ensure some random and invalid information is not stored in database. 

4. Booking History
In this API, the user email and type are taken as params of GET request. Initially the validate of user is done and then booking details of user are serialized and returned.
 
Also, some checks are also made like whether is registered and have a verified profile. Similarly, for drivers also, these checks are done.

5. All available cabs
In this API, I am trying to get all available cabs using a GET request. A serialized response is returned from the API.

Also, I have tried to make another version of this API considering the location paramters but was not able to completely test it and get desired results.

6. Book Cab
In this API, the details of driver, starting point and ending point, cab type and status of cab are sent in body of POST request.

Initially, the status of the cab is checked along with the cab type to find if the cab is available and the status is not riding or booked. If the cab is then available then it is assigned to the customer and serialized cab details are returned from the API.

