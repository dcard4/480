CREATE TABLE Librarians (
    ssn INT PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR UNIQUE NOT NULL,
    salary NUMERIC NOT NULL
);


CREATE TABLE Clients (
    email VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    password VARCHAR UNIQUE NOT NULL
);


CREATE TABLE ClientAddresses (
    email VARCHAR,
    address VARCHAR,
	FOREIGN KEY (email) REFERENCES Clients,
	PRIMARY KEY (email, address)
);


CREATE TABLE CreditCards (
    email VARCHAR,
	address VARCHAR,
	number INT,
	FOREIGN KEY (email) REFERENCES Clients,
	PRIMARY KEY (email, address, number)
);


CREATE TABLE Documents (
    barcode INT PRIMARY KEY,
    copies INT NOT NULL,
    publisher VARCHAR NOT NULL,
    year INT
);

CREATE TABLE NonJournal (
    isbn INT PRIMARY KEY,
    barcode INT NOT NULL,
    FOREIGN KEY (barcode) REFERENCES Documents
);

CREATE TABLE Journal (
    title VARCHAR,
    issue INT,
    name VARCHAR NOT NULL, 
    authors VARCHAR NOT NULL,
    number INT NOT NULL,
    barcode INT NOT NULL,
    FOREIGN KEY (barcode) REFERENCES Documents,
    PRIMARY KEY (title, issue)
);

CREATE TABLE Book (
    isbn INT PRIMARY KEY,
    title VARCHAR NOT NULL,
    authors VARCHAR NOT NULL,
    edition INT NOT NULL,
    pages INT NOT NULL,
    FOREIGN KEY (isbn) REFERENCES NonJournal
);

CREATE TABLE Magazine (
    isbn INT PRIMARY KEY,
    name VARCHAR NOT NULL,
    month VARCHAR NOT NULL,
    FOREIGN KEY (isbn) REFERENCES NonJournal
);

CREATE TABLE BorrowedDocuments (
    barcode INT,
    email VARCHAR,
    due DATE NOT NULL,
    checkout DATE NOT NULL,
    fee INT NOT NULL,
    FOREIGN KEY (email) REFERENCES Clients,
    PRIMARY KEY (email, barcode)
);


CREATE INDEX document_barcode ON Documents(barcode);
CREATE INDEX client_email on Clients(email);
CREATE INDEX librarian_ssn ON Librarians(ssn);
CREATE INDEX librarian_email ON Librarians(email);