-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema monitor
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema monitor
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `monitor` DEFAULT CHARACTER SET utf8 ;
USE `monitor` ;

-- -----------------------------------------------------
-- Table `monitor`.`clients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `monitor`.`clients` (
  `ipclient` VARCHAR(15) NOT NULL,
  `cpu` FLOAT NOT NULL,
  `memory` FLOAT NOT NULL,
  `uptime` INT(11) NOT NULL,
  `sec_logs` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`ipclient`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `monitor`.`alerts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `monitor`.`alerts` (
  `clients_ipclient` VARCHAR(15) NOT NULL,
  `type` ENUM('memory', 'cpu') NOT NULL,
  `limit` INT NOT NULL,
  PRIMARY KEY (`clients_ipclient`),
  INDEX `fk_alerts_clients_idx` (`clients_ipclient` ASC),
  CONSTRAINT `fk_alerts_clients`
    FOREIGN KEY (`clients_ipclient`)
    REFERENCES `monitor`.`clients` (`ipclient`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
