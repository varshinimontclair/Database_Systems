CREATE DATABASE llc_tax_payment_system;
USE llc_tax_payment_system;

CREATE TABLE TaxBreakDown (
	Id INT AUTO_INCREMENT NOT NULL,
    Company VARCHAR(255) NOT NULL,
    Amount VARCHAR(255) NOT NULL,
    PaymentDate VARCHAR(255) NOT NULL,
    Status VARCHAR(255) NOT NULL,
    DueDate VARCHAR(255) NOT NULL,
    PRIMARY KEY (Id)
);

