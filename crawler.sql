DROP DATABASE IF EXISTS crawler;
CREATE DATABASE crawler;
USE crawler;


CREATE TABLE url
(
    url_id INT NOT NULL AUTO_INCREMENT,
    url VARCHAR(100) UNIQUE,
    counter INT NOT NULL,
    PRIMARY KEY (url_id)
);


CREATE TABLE domain
(
    domain_id INT NOT NULL AUTO_INCREMENT,
    domain VARCHAR(100) UNIQUE,
    counter INT NOT NULL,
    url VARCHAR(100),
    PRIMARY KEY (domain_id),
    FOREIGN KEY (url) REFERENCES url(url)
);

CREATE TABLE blocked_domain
(
    domain_id INT NOT NULL AUTO_INCREMENT,
    domain VARCHAR(100) UNIQUE,
    counter INT NOT NULL,
    url VARCHAR(100),
    PRIMARY KEY (domain_id),
    FOREIGN KEY (url) REFERENCES url(url)
);

CREATE TABLE integer_ip
(
    ip VARCHAR(100) NOT NULL,
    counter INT NOT NULL,
    domain VARCHAR(100),
    url VARCHAR(100),
    PRIMARY KEY (ip),
    FOREIGN KEY (url) REFERENCES url(url)
);

CREATE TABLE cidr_ips
(
    ip VARCHAR(100) NOT NULL,
    counter INT NOT NULL,
    url VARCHAR(100),
    PRIMARY KEY (ip),
    FOREIGN KEY (url) REFERENCES url(url)
);



CREATE TABLE filtered_mails
(
    mail_id INT NOT NULL AUTO_INCREMENT,
    mail VARCHAR(100) UNIQUE,
    counter INT NOT NULL,
    url VARCHAR(100),
    PRIMARY KEY (mail_id),
    FOREIGN KEY (url) REFERENCES url(url)
);

