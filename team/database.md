数据库字典: thuactivities
-----
斜体为*索引*

加粗为**主键**
已添加外键，尚未添加索引

# schedule
* ***id***
* user_id: foreign key
* activity_id: foreign key
* seat_id: foreign key
* ticket: QR code
* presence: whether present in the activity


# user
* ***id***
* name
* gender
* telephone
* wechat_id
* verified: whether verified by administrator
* priority


# activity
* ***id***
* title
* time
* description
* number_of_tickets
* tickets_sold: number of tickets sold
* classroom_id: foreign key


# activity_preference
not constructed yet
* ***user_id***
* ***activity_id***
* prefer_time


# classroom
* ***id***
* name


# seat
* ***id***
* classroom_id: foreign_key
* name

