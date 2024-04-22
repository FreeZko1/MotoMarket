    use omegadbdva;

    CREATE TABLE Users (
        UserID INT AUTO_INCREMENT PRIMARY KEY,
        FirstName VARCHAR(50),
        LastName VARCHAR(50),
        Email VARCHAR(100) UNIQUE,
        Password VARCHAR(100),
        PhoneNumber VARCHAR(15),
        Role ENUM('Admin', 'User') NOT NULL  -- Zjednodušené na Admin a User
    );

    CREATE TABLE Vehicles (
        VehicleID INT AUTO_INCREMENT PRIMARY KEY,
        Brand VARCHAR(50),
        Model VARCHAR(50),
        YearOfManufacture YEAR,
        Mileage INT,
        Price DECIMAL(10, 2),
        UserID INT,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );

    CREATE TABLE VehicleImages (
        ImageID INT AUTO_INCREMENT PRIMARY KEY,
        VehicleID INT,
        ImageData BLOB,
        FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
    );


    CREATE TABLE Sales (
        SaleID INT AUTO_INCREMENT PRIMARY KEY,
        VehicleID INT,
        SellerUserID INT,
        BuyerUserID INT,
        SaleDate DATE,
        SalePrice DECIMAL(10, 2),
        FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID),
        FOREIGN KEY (SellerUserID) REFERENCES Users(UserID),
        FOREIGN KEY (BuyerUserID) REFERENCES Users(UserID)
    );

    CREATE TABLE Reviews (
        id INT AUTO_INCREMENT PRIMARY KEY,
        author_id INT,
        user_id INT,
        content TEXT,
        rating INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (author_id) REFERENCES users(UserID),
        FOREIGN KEY (user_id) REFERENCES users(UserID)
    );

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


    DESCRIBE users;


    ALTER TABLE users ADD COLUMN username VARCHAR(255);
    ALTER TABLE Vehicles ADD Description TEXT;


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
