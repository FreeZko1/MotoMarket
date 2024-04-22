-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: omegadbdva
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Position to start replication or point-in-time recovery from
--

-- CHANGE MASTER TO MASTER_LOG_FILE='VBOOK-bin.000011', MASTER_LOG_POS=157;

--
-- Table structure for table `chatmessages`
--

DROP TABLE IF EXISTS `chatmessages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4_general_ci */;
CREATE TABLE `chatmessages` (
  `MessageID` int NOT NULL AUTO_INCREMENT,
  `SenderUserID` int DEFAULT NULL,
  `RecipientUserID` int DEFAULT NULL,
  `MessageText` text,
  `Timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`MessageID`),
  KEY `SenderUserID` (`SenderUserID`),
  KEY `RecipientUserID` (`RecipientUserID`),
  CONSTRAINT `chatmessages_ibfk_1` FOREIGN KEY (`SenderUserID`) REFERENCES `users` (`UserID`),
  CONSTRAINT `chatmessages_ibfk_2` FOREIGN KEY (`RecipientUserID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4_general_ci COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatmessages`
--
-- ORDER BY:  `MessageID`

LOCK TABLES `chatmessages` WRITE;
/*!40000 ALTER TABLE `chatmessages` DISABLE KEYS */;
INSERT INTO `chatmessages` VALUES (1,1,2,'Ahoj, jak se máš?','2024-04-19 13:14:03'),(2,1,6,'sss','2024-04-20 19:21:31'),(3,1,6,'ahoj\n','2024-04-20 19:44:18'),(4,6,1,'wassup','2024-04-20 19:58:45'),(5,6,1,'kamo funguje to!!','2024-04-20 20:05:46');
/*!40000 ALTER TABLE `chatmessages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4_general_ci */;
CREATE TABLE `news` (
  `NewsID` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(255) DEFAULT NULL,
  `Description` text,
  `ActionURL` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`NewsID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4_general_ci COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--
-- ORDER BY:  `NewsID`

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
INSERT INTO `news` VALUES (1,'Hledáme admina','Naše stránka hledá nového administrátora. Pokud máte zájem, klikněte pro více informací.','url_kde_se_mohou_uchazeči_přihlásit'),(2,'Hledáme vývojáře','Přidejte se k našemu týmu jako vývojář. Klikněte zde pro podrobnosti a přihlášení.','url_kde_se_mohou_uchazeči_přihlásit');
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4_general_ci */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `author_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `content` text,
  `rating` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`UserID`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4_general_ci COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--
-- ORDER BY:  `id`

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,1,1,'docela frajer',3,'2024-04-18 00:14:34'),(2,1,6,'docela mě sere',5,'2024-04-20 10:11:54'),(3,5,1,'chci ti smazat profil',4,'2024-04-20 22:12:23');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4_general_ci */;
CREATE TABLE `sales` (
  `SaleID` int NOT NULL AUTO_INCREMENT,
  `VehicleID` int DEFAULT NULL,
  `SellerUserID` int DEFAULT NULL,
  `BuyerUserID` int DEFAULT NULL,
  `SaleDate` date DEFAULT NULL,
  `SalePrice` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`SaleID`),
  KEY `VehicleID` (`VehicleID`),
  KEY `SellerUserID` (`SellerUserID`),
  KEY `BuyerUserID` (`BuyerUserID`),
  CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`VehicleID`) REFERENCES `vehicles` (`VehicleID`),
  CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`SellerUserID`) REFERENCES `users` (`UserID`),
  CONSTRAINT `sales_ibfk_3` FOREIGN KEY (`BuyerUserID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4_general_ci COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--
-- ORDER BY:  `SaleID`

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4_general_ci */;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `PhoneNumber` varchar(15) DEFAULT NULL,
  `Role` enum('Admin','User') NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `AboutMe` text,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4_general_ci COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--
-- ORDER BY:  `UserID`

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'honzaJeDementjakpica','Nováks','jan.novak@example.com','heslo123','123456789','User',NULL,'jsem honza vyzzli wizzard a smrdim'),(2,'Eva','Svobodová','eva.svobodova@example.com','tajneHeslo','987654321','User',NULL,NULL),(3,'Petr','Veselý','petr.vesely@example.com','superTajne','111223344','Admin',NULL,NULL),(4,NULL,NULL,'prosim.funguj@email.com','heslokleslo',NULL,'Admin','username1',NULL),(5,NULL,NULL,'jauznevim@seznam.cz','peklostroj',NULL,'Admin','uzivateljmeno',NULL),(6,'Pepa','Mrázek','pepik.freez@gmail.com','nevimheslo','125489666','User','freezko',NULL),(8,'Štěpán ','Laichiter','stepan.laichter@gmail.com','Stepan1','965874213','User','steepix',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehiclehistory`
--

DROP TABLE IF EXISTS `vehiclehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4_general_ci */;
CREATE TABLE `vehiclehistory` (
  `HistoryID` int NOT NULL AUTO_INCREMENT,
  `VehicleID` int DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Description` text,
  `Type` enum('Maintenance','Accident','Upgrade','Other') DEFAULT NULL,
  `Cost` decimal(10,2) DEFAULT NULL,
  `Document` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`HistoryID`),
  KEY `VehicleID` (`VehicleID`),
  CONSTRAINT `vehiclehistory_ibfk_1` FOREIGN KEY (`VehicleID`) REFERENCES `vehicles` (`VehicleID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4_general_ci COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehiclehistory`
--
-- ORDER BY:  `HistoryID`

LOCK TABLES `vehiclehistory` WRITE;
/*!40000 ALTER TABLE `vehiclehistory` DISABLE KEYS */;
INSERT INTO `vehiclehistory` VALUES (1,14,'2021-02-02','chip','Upgrade',35000.00,NULL),(2,14,'2023-07-17','bOuraČka','Accident',120000.00,NULL),(3,14,'2023-07-17','bOuraČka','Accident',120000.00,NULL),(4,14,'2021-05-12','cras','Accident',120000.00,NULL),(5,14,'2024-02-20','nevim','Maintenance',45.00,NULL),(6,14,'2024-07-17','totalka','Accident',2000000.00,NULL),(7,14,'2024-07-17','nevim','Upgrade',45000.00,NULL),(8,18,'2024-04-14','Skočil mi do cesty strom','Accident',1000.00,NULL);
/*!40000 ALTER TABLE `vehiclehistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicleimages`
--

DROP TABLE IF EXISTS `vehicleimages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4_general_ci */;
CREATE TABLE `vehicleimages` (
  `ImageID` int NOT NULL AUTO_INCREMENT,
  `VehicleID` int DEFAULT NULL,
  `ImageData` longblob,
  PRIMARY KEY (`ImageID`),
  KEY `VehicleID` (`VehicleID`),
  CONSTRAINT `vehicleimages_ibfk_1` FOREIGN KEY (`VehicleID`) REFERENCES `vehicles` (`VehicleID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4_general_ci COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicleimages`
--
-- ORDER BY:  `ImageID`

LOCK TABLES `vehicleimages` WRITE;
/*!40000 ALTER TABLE `vehicleimages` DISABLE KEYS */;
INSERT INTO `vehicleimages` VALUES (1,7,NULL);
INSERT INTO `vehicleimages` VALUES (2,8,NULL);
INSERT INTO `vehicleimages` VALUES (3,9,NULL),(6,14,NULL);
INSERT INTO `vehicleimages` VALUES (7,15,NULL);
INSERT INTO `vehicleimages` VALUES (8,18,NULL),(9,20,NULL);
/*!40000 ALTER TABLE `vehicleimages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehiclereviews`
--

DROP TABLE IF EXISTS `vehiclereviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4_general_ci */;
CREATE TABLE `vehiclereviews` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `vehicle_id` int NOT NULL,
  `author_id` int NOT NULL,
  `content` text NOT NULL,
  `rating` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  KEY `vehicle_id` (`vehicle_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `vehiclereviews_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`VehicleID`),
  CONSTRAINT `vehiclereviews_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `users` (`UserID`),
  CONSTRAINT `vehiclereviews_chk_1` CHECK (((`rating` >= 1) and (`rating` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4_general_ci COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehiclereviews`
--
-- ORDER BY:  `review_id`

LOCK TABLES `vehiclereviews` WRITE;
/*!40000 ALTER TABLE `vehiclereviews` DISABLE KEYS */;
  INSERT INTO `vehiclereviews` VALUES (1,14,1,'smrdis',1,'2024-04-18 19:22:39'),(2,14,1,'stocenka',1,'2024-04-18 19:23:21'),(3,15,1,'drift missle',5,'2024-04-18 21:02:37');
/*!40000 ALTER TABLE `vehiclereviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicles`
--

DROP TABLE IF EXISTS `vehicles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4_general_ci */;
CREATE TABLE `vehicles` (
  `VehicleID` int NOT NULL AUTO_INCREMENT,
  `Brand` varchar(50) DEFAULT NULL,
  `Model` varchar(50) DEFAULT NULL,
  `YearOfManufacture` year DEFAULT NULL,
  `Mileage` int DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `UserID` int DEFAULT NULL,
  `Description` text,
  PRIMARY KEY (`VehicleID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4_general_ci COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicles`
--
-- ORDER BY:  `VehicleID`

LOCK TABLES `vehicles` WRITE;
/*!40000 ALTER TABLE `vehicles` DISABLE KEYS */;
INSERT INTO `vehicles` VALUES (1,'Toyota','Corolla',2018,50000,15000.00,NULL,NULL),(2,'Ford','Fiesta',2017,60000,8000.00,NULL,NULL),(3,'Volkswagen','Golf',2019,30000,18000.00,NULL,NULL),(4,'Škoda','Octavia',2020,25000,20000.00,NULL,NULL),(5,'Honda','Civic',2016,80000,12000.00,NULL,NULL),(7,'VolksWagen','Golf',2000,160000,45000.00,NULL,NULL),(8,'VolksWagen','Golf',2000,160000,45000.00,NULL,NULL),(9,'škoda','Octavia',2004,450000,10000000.00,NULL,NULL),(14,'audi','RS6',2020,5000,4000000.00,1,NULL),(15,'nissan','240sx',1990,280000,899000.00,6,NULL),(16,'sss','Golf',2003,420,420.00,1,NULL),(17,'sss','Golf',2005,13855,12356.00,1,NULL),(18,'Škoda','Fabia',2001,140000,15000.00,8,NULL),(19,'sss','sss',2005,520000,522000.00,1,NULL),(20,'sss','ssss',2005,202220,42069.00,1,NULL);
/*!40000 ALTER TABLE `vehicles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-21 20:12:17
