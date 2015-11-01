数据库字典
-----
斜体为*索引*
加粗为**主键**


# Table_Schedule
* ***Schedule_ID***
* User_ID
* Activity_ID
* Schedule_Seat_ID
* Schedule_Ticket
* Schedule_Presence


# Table_User
* ***User_ID***
* User_Name
* User_Gender
* User_Telephone
* User_Approval
* User_Priority


# Table_Activity
* ***Activity_ID***
* Activity_Title
* Activity_Time
* Activity_Guest
* Activity_Description
* Activity_Ticket_Start
* Activity_Ticket_End
* Classroom_ID


# Table_Activity_Like
* ***User_ID***
* ***Activity_ID***
* Like_Time


# Table_Classroom_
* ***Classroom_ID***
* Classroom_Name


# Table_Seat
* ***Seat ID***
* *Classroom_ID*
* Seat_Name

