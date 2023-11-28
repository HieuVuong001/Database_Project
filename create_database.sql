create table member(
    username varchar(45) NOT NULL,
    membership_type varchar(45) NOT NULL,
    pw varbinary(1024) NOT NULL, 
    date_joined DATETIME NOT NULL, 
    PRIMARY KEY(username)); 

create table admin(
    username varchar(45) NOT NULL,
    PRIMARY KEY(username),
    FOREIGN KEY(username) REFERENCES member(username));

create table portfolio(
    username varchar(45) NOT NULL, 
    portfolio_name varchar(45) NOT NULL, 
    PRIMARY KEY(username, portfolio_name), 
    FOREIGN KEY(username) REFERENCES member(username) ON UPDATE CASCADE ON DELETE CASCADE
    );

create table post(
    pid int NOT NULL AUTO_INCREMENT,
    content varchar(1024) NOT NULL,
    username varchar(45) NOT NULL,
    date_created DATETIME NOT NULL,
    PRIMARY KEY(pid, username),
    FOREIGN KEY(username) REFERENCES member(username) ON UPDATE CASCADE ON DELETE CASCADE
);

create table keyboard(
    kb_name varchar(45) NOT NULL,
    theme varchar(45),
    plate varchar(45),
    kb_case varchar(45),
    pcb varchar(45),
    keycaps varchar(45),
    stabilizers varchar(45),
    switches varchar(45),
    portfolio_name varchar(45) NOT NULL,
    username varchar(45) NOT NULL,
    PRIMARY KEY(kb_name, portfolio_name, username),
    FOREIGN KEY(username, portfolio_name) REFERENCES portfolio(username, portfolio_name) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(username) REFERENCES member(username) ON UPDATE CASCADE ON DELETE CASCADE
);

create table builder(
    username varchar(45) NOT NULL,
    quantity_built int NOT NULL,
    specialty varchar(90),
    builder_type varchar(45) NOT NULL,
    interest varchar(45),
    PRIMARY KEY(username)
);

create table user_builds(
    username varchar(45) NOT NULL,
    kb_name varchar(45) NOT NULL,
    PRIMARY KEY(username),
    FOREIGN KEY(kb_name) REFERENCES keyboard(kb_name) ON UPDATE CASCADE ON DELETE CASCADE
);

create table workshop(
    wid int NOT NULL AUTO_INCREMENT,
    workshop_name varchar(45) NOT NULL,
    capacity int NOT NULL,
    requirements  varchar(255) NOT NULL,
    PRIMARY KEY(wid)
);

create table contest(
    cid int NOT NULL AUTO_INCREMENT,
    contest_name varchar(45) NOT NULL,
    capacity int NOT NULL,
    requirements varchar(255) NOT NULL,
    date_created DATETIME NOT NULL,
    PRIMARY KEY(cid)
);

create table organization(
    org_name varchar(45) NOT NULL,
    number_members int NOT NULL,
    style varchar(45) NOT NULL,
    username varchar(45) NOT NULL,
    PRIMARY KEY(org_name, username),
    FOREIGN KEY(username) REFERENCES member(username) ON UPDATE CASCADE
);

create table workshop_host(
    username varchar(45) NOT NULL,
    wid int NOT NULL,
    start_date DATETIME NOT NULL,
    PRIMARY KEY(username, wid),
    FOREIGN KEY(username) REFERENCES member(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(wid) REFERENCES workshop(wid) ON UPDATE CASCADE ON DELETE CASCADE 
);

create table workshop_join(
    username varchar(45) NOT NULL,
    wid int NOT NULL,
    PRIMARY KEY(username, wid),
    FOREIGN KEY(username) REFERENCES member(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(wid) REFERENCES workshop(wid) ON UPDATE CASCADE ON DELETE CASCADE 
);

create table contest_participants(
    username varchar(45) NOT NULL,
    cid int NOT NULL,
    PRIMARY KEY(username, cid),
    FOREIGN KEY(username) REFERENCES member(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(cid) REFERENCES contest(cid) ON DELETE CASCADE
);

create table contest_host(
    username varchar(45) NOT NULL,
    cid int NOT NULL,
    contest_reward varchar(255) NOT NULL,
    PRIMARY KEY(username, cid),
    FOREIGN KEY(username) REFERENCES member(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(cid) REFERENCES contest(cid) ON DELETE CASCADE
);

create table post_like(
    username varchar(45) NOT NULL,
    pid int NOT NULL,
    created_date DATETIME NOT NULL,
    PRIMARY KEY(username, pid),
    FOREIGN KEY(username) REFERENCES member(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(pid) REFERENCES post(pid) ON UPDATE CASCADE ON DELETE CASCADE
);


create table post_comment(
    username varchar(45) NOT NULL,
    pid int NOT NULL,
    created_date DATETIME NOT NULL,
    content varchar(255) NOT NULL,
    PRIMARY KEY(username, pid),
    FOREIGN KEY(username) REFERENCES member(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(pid) REFERENCES post(pid) ON UPDATE CASCADE ON DELETE CASCADE
);
