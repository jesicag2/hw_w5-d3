CREATE DATABASE fitness_tracker;

USE fitness_tracker;

CREATE TABLE Members (
	member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    membership_type VARCHAR(30)
);

CREATE TABLE Workout_sesh (
	sesh_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    member_id INT,
    workout_type VARCHAR(501),
	FOREIGN KEY (member_id) REFERENCES members(member_id)
);

INSERT INTO Members (name, email, phone, membership_type)
VALUES ("Goku", "songoku@gmail.com", "3051234567", "Platinum Status");

INSERT INTO Workout_sesh (date, member_id, workout_type)
VALUES ("2024-04-10", 1, "Strength");

SELECT *
FROM Workout_sesh;

SELECT *
FROM Members;

