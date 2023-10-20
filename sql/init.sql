CREATE TABLE IF NOT EXISTS Departments
(
 department_id       INT NOT NULL,
 department_name     TEXT NOT NULL,
 manager_id          INT NOT NULL,
 CONSTRAINT PK_1 PRIMARY KEY (department_id)
);

CREATE TABLE IF NOT EXISTS Users
(
 user_id                     INT NOT NULL,
 user_first_name             TEXT NOT NULL,
 user_last_name              TEXT NOT NULL,
 user_phone_number           INT NOT NULL,
 user_date_of_birth          DATE NOT NULL,
 user_encrypted_password     TEXT NOT NULL,
 user_created_at             TIMESTAMP WITH TIME ZONE NOT NULL,
 user_updated_at             TIMESTAMP WITH TIME ZONE NOT NULL,
 user_last_connected         TIMESTAMP WITH TIME ZONE NOT NULL,
 user_email                  TEXT NOT NULL,
 phone                       TEXT NOT NULL,
 CONSTRAINT PK_2 PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS Employees
(
 employee_id       INT NOT NULL,
 first_name        TEXT NOT NULL,
 last_name         TEXT NOT NULL,
 email             TEXT NOT NULL,
 phone_number      INT NOT NULL,
 date_of_birth     DATE NOT NULL,
 department_id     INT NOT NULL,
 salary            INT NOT NULL,
 CONSTRAINT PK_3 PRIMARY KEY (employee_id),
 CONSTRAINT FK_14_2 FOREIGN KEY (department_id) REFERENCES Departments (department_id)
);


CREATE TABLE IF NOT EXISTS "Moderation Department"
(
 moderator_id      INT NOT NULL,
 post_id           INT NOT NULL,
 meeting_id        INT NOT NULL,
 department_id     INT NOT NULL,
 employee_id       INT NOT NULL,
 CONSTRAINT PK_4 PRIMARY KEY (moderator_id),
 CONSTRAINT FK_14 FOREIGN KEY (department_id) REFERENCES Departments (department_id),
 CONSTRAINT FK_14_1 FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
);

CREATE TABLE IF NOT EXISTS "Human Resources Department"
(
 resources_id      INT NOT NULL,
 department_id     INT NOT NULL,
 employee_id       INT NOT NULL,
 CONSTRAINT PK_5 PRIMARY KEY (resources_id),
 CONSTRAINT FK_17 FOREIGN KEY (department_id) REFERENCES Departments (department_id),
 CONSTRAINT FK_18 FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
);

CREATE TABLE IF NOT EXISTS Posts
(
 post_id          INT NOT NULL,
 post_title       TEXT NOT NULL,
 moderator_id     INT NOT NULL,
 created_at       TIMESTAMP WITH TIME ZONE NOT NULL,
 user_id          INT NOT NULL,
 CONSTRAINT PK_6 PRIMARY KEY (post_id),
 CONSTRAINT FK_12 FOREIGN KEY (moderator_id) REFERENCES "Moderation Department" (moderator_id),
 CONSTRAINT FK_16_2 FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE IF NOT EXISTS Comments
(
 comment_id        INT NOT NULL,
 comment_desc      TEXT NOT NULL,
 post_id           INT NOT NULL,
 user_id           INT NOT NULL,
 created_at        TIMESTAMP WITH TIME ZONE NOT NULL,
 last_modified     TIMESTAMP WITH TIME ZONE NOT NULL,
 CONSTRAINT PK_7 PRIMARY KEY (comment_id),
 CONSTRAINT FK_15 FOREIGN KEY (post_id) REFERENCES Posts (post_id),
 CONSTRAINT FK_16 FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE IF NOT EXISTS Customer
(
 customer_id     INT NOT NULL,
 user_id_1       INT NOT NULL,
 CONSTRAINT PK_8 PRIMARY KEY (customer_id),
 CONSTRAINT FK_4 FOREIGN KEY (user_id_1) REFERENCES Users (user_id)
);

CREATE TABLE IF NOT EXISTS "Sales Moderation Department"
(
 sales_rep_id      INT NOT NULL,
 sale_id           INT NOT NULL,
 manager_id        INT NOT NULL,
 department_id     INT NOT NULL,
 employee_id       INT NOT NULL,
 CONSTRAINT PK_9 PRIMARY KEY (sales_rep_id),
 CONSTRAINT FK_13 FOREIGN KEY (department_id) REFERENCES Departments (department_id),
 CONSTRAINT FK_18_1 FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
);

CREATE TABLE IF NOT EXISTS Seller
(
 seller_id     INT NOT NULL,
 user_id       INT NOT NULL,
 CONSTRAINT PK_10 PRIMARY KEY (seller_id),
 CONSTRAINT FK_3 FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE IF NOT EXISTS Marketplace
(
 sale_id          INT NOT NULL,
 sale_title       TEXT NOT NULL,
 sale_desc        TEXT NOT NULL,
 sale_price       FLOAT NOT NULL,
 customer_id      INT NOT NULL,
 seller_id        INT NOT NULL,
 sales_rep_id     INT NOT NULL,
 CONSTRAINT PK_11 PRIMARY KEY (sale_id),
 CONSTRAINT FK_14_3 FOREIGN KEY (seller_id) REFERENCES Seller (seller_id),
 CONSTRAINT FK_18_2 FOREIGN KEY (sales_rep_id) REFERENCES "Sales Moderation Department" (sales_rep_id),
 CONSTRAINT FK_6 FOREIGN KEY (customer_id) REFERENCES Customer (customer_id)
);

CREATE TABLE IF NOT EXISTS Meetings
(
 meeting_id       INT NOT NULL,
 moderator_id     INT NOT NULL,
 meeting_name     TEXT NOT NULL,
 meeting_date     DATE NOT NULL,
 meeting_desc     TEXT NOT NULL,
 user_id          INT NOT NULL,
 CONSTRAINT PK_12 PRIMARY KEY (meeting_id),
 CONSTRAINT FK_11 FOREIGN KEY (moderator_id) REFERENCES "Moderation Department" (moderator_id),
 CONSTRAINT FK_16_1 FOREIGN KEY (user_id) REFERENCES Users (user_id)
);
