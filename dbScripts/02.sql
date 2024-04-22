use omegadbdva;

ALTER TABLE users ADD COLUMN username VARCHAR(255);

describe users;

INSERT INTO Users (FirstName, LastName, Email, Password, PhoneNumber, Role) VALUES
('Jan', 'Novák', 'jan.novak@example.com', 'heslo123', '123456789', 'User'),
('Eva', 'Svobodová', 'eva.svobodova@example.com', 'tajneHeslo', '987654321', 'User'),
('Petr', 'Veselý', 'petr.vesely@example.com', 'superTajne', '111223344', 'Admin');

SELECT * FROM users;
DELETE users FROM users WHERE UserID = 7;


CREATE TABLE VehicleImages (
    ImageID INT AUTO_INCREMENT PRIMARY KEY,
    VehicleID INT,
    ImageData BLOB,
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
);


ALTER TABLE VehicleImages MODIFY ImageData LONGBLOB;

select * from vehicles;

select * from VehicleImages;




INSERT INTO Vehicles (Brand, Model, YearOfManufacture, Mileage, Price) VALUES
('Toyota', 'Corolla', 2018, 50000, 15000.00),
('Ford', 'Fiesta', 2017, 60000, 8000.00),
('Volkswagen', 'Golf', 2019, 30000, 18000.00),
('Škoda', 'Octavia', 2020, 25000, 20000.00),
('Honda', 'Civic', 2016, 80000, 12000.00);

describe vehicles;
select * from vehicles;

drop table VehicleImages;


SELECT v.VehicleID, v.Brand, v.Model, v.YearOfManufacture, v.Mileage, v.Price, vi.ImageData 
FROM Vehicles v 
LEFT JOIN VehicleImages vi ON v.VehicleID = vi.VehicleID;


SELECT v.VehicleID, v.Brand, v.Model, v.YearOfManufacture, v.Mileage, v.Price, vi.ImageData 
FROM Vehicles v 
LEFT JOIN VehicleImages vi ON v.VehicleID = vi.VehicleID;


SELECT v.VehicleID, v.Brand, v.Model, v.YearOfManufacture, v.Mileage, v.Price, vi.ImageData 
FROM Vehicles v 
LEFT JOIN VehicleImages vi ON v.VehicleID = vi.VehicleID;


select * from vehicles;

describe users;

ALTER TABLE Vehicles ADD Description TEXT;





ALTER TABLE Users ADD AboutMe TEXT;

describe vehicles;


SELECT v.VehicleID, v.Brand, v.Model, v.YearOfManufacture, v.Mileage, v.Price, v.Description,
       u.FirstName, u.LastName
FROM Vehicles v
JOIN Users u ON v.UserID = u.UserID
WHERE v.VehicleID = 1 ; -- nahraďte 1 skutečným ID pro test

select * from users;

SELECT * FROM Vehicles WHERE VehicleID = 1;

SELECT * FROM Users WHERE UserID = (SELECT UserID FROM Vehicles WHERE VehicleID = 1);

CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    user_id INT,
    content TEXT,
    rating INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(UserID),
    FOREIGN KEY (user_id) REFERENCES users(UserID)
);

select * from reviews;

CREATE TABLE VehicleHistory (
    HistoryID INT AUTO_INCREMENT PRIMARY KEY,
    VehicleID INT,
    Date DATE,
    Description TEXT,
    Type ENUM('Maintenance', 'Accident', 'Upgrade', 'Other'),
    Cost DECIMAL(10, 2),
    Document VARCHAR(255),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
);


CREATE TABLE VehicleReviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    author_id INT NOT NULL,
    content TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(VehicleID),
    FOREIGN KEY (author_id) REFERENCES Users(UserID)
);

select * from vehicles;

INSERT INTO chatmessages (SenderUserID, RecipientUserID, MessageText, Timestamp)
VALUES (1, 2, 'Ahoj, jak se máš?', NOW());

describe vehicles;

delete from news where newsid = 4;

CREATE TABLE News (
    NewsID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    Description TEXT,
    ActionURL VARCHAR(255)
);

CREATE TABLE ChatMessages (
    MessageID INT AUTO_INCREMENT PRIMARY KEY,
    SenderUserID INT,
    RecipientUserID INT,
    MessageText TEXT,
    Timestamp DATETIME,
    FOREIGN KEY (SenderUserID) REFERENCES Users(UserID),
    FOREIGN KEY (RecipientUserID) REFERENCES Users(UserID)
);


CREATE TABLE ads (
    ad_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    image_url VARCHAR(255),
    target_url VARCHAR(255),
    start_date DATE,
    end_date DATE,
    active BOOLEAN
);


describe omegadbdva;

INSERT INTO News (Title, Description, ActionURL) VALUES
('Hledáme admina', 'Naše stránka hledá nového administrátora. Pokud máte zájem, klikněte pro více informací.', 'url_kde_se_mohou_uchazeči_přihlásit'),
('Hledáme vývojáře', 'Přidejte se k našemu týmu jako vývojář. Klikněte zde pro podrobnosti a přihlášení.', 'url_kde_se_mohou_uchazeči_přihlásit');

SELECT * FROM VehicleHistory WHERE VehicleID = 14 ORDER BY Date DESC;
