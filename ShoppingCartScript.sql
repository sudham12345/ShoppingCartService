
CREATE SCHEMA shoppingcart;
ALTER SCHEMA shoppingcart OWNER TO tinitiate;
set search_path=shoppingcart;

CREATE TABLE shoppingcart.products
(prod_id int not null,
prod_category varchar(50) not null,
prod_name varchar(50) not null,
prod_price decimal(10,2) not null,
prod_create_date date,
primary key(prod_id)
);

CREATE TABLE shoppingcart.cart
(cart_id int not null,
cookie_uuid varchar(50) not null,
prod_id int, 
prod_name varchar(50),
prod_qty int,
prod_price decimal(10,2),
create_date date,
update_date date,
primary key(cart_id)
);

CREATE TABLE shoppingcart.user_cart
(cart_id int not null,
user_id int not null,
prod_id int, 
prod_name varchar(50),
prod_qty int,
prod_price decimal(10,2),
create_date date,
update_date date,
primary key(cart_id)
);

CREATE TABLE shoppingcart.orders
(order_id int not null,
user_id int not null,
create_date date,
primary key (order_id)
);

CREATE TABLE shoppingcart.order_details
(order_details_id int not null,
order_id int not null,
prod_id int, 
prod_name varchar(50),
prod_qty int,
prod_price decimal(10,2),
primary key (order_details_id),
foreign key (order_id) references orders(order_id)
);

CREATE TABLE shoppingcart.user
(user_id int not null,
user_name varchar(50) not null,
primary key (user_id)
)

INSERT into shoppingcart.user values(11110001,'ABC');
INSERT into shoppingcart.user values(11110002,'XYZ');
 

INSERT into shoppingcart.products values (1001,'Fruits','Apple',2.99,'2021-01-25');
INSERT into shoppingcart.products values (1002,'Fruits','Orange',3.99,'2021-01-25');
INSERT into shoppingcart.products values (1003,'Fruits','Grapes',5.99,'2021-01-25');
INSERT into shoppingcart.products values (1004,'Fruits','Pears',6.99,'2021-01-25');
INSERT into shoppingcart.products values (1005,'Fruits','Banana',2.99,'2021-01-25');
INSERT into shoppingcart.products values (2001,'Vegetables','Potato',2.99,'2021-01-25');
INSERT into shoppingcart.products values (2002,'Vegetables','Tomatoes',2.99,'2021-01-25');
INSERT into shoppingcart.products values (2003,'Vegetables','Onions',2.99,'2021-01-25');
INSERT into shoppingcart.products values (2004,'Vegetables','Carrots',3.99,'2021-01-25');
INSERT into shoppingcart.products values (2005,'Vegetables','Beans',2.99,'2021-01-25');
INSERT into shoppingcart.products values (3001,'Snacks','Chips',2.99,'2021-01-25');
INSERT into shoppingcart.products values (3002,'Snacks','Cookies',3.99,'2021-01-25');
INSERT into shoppingcart.products values (3003,'Snacks','Popcorn',2.99,'2021-01-25');
INSERT into shoppingcart.products values (3004,'Snacks','Pretzels',2.99,'2021-01-25');
INSERT into shoppingcart.products values (3005,'Snacks','Candy',2.99,'2021-01-25');
INSERT into shoppingcart.products values (4001,'Beverages','Juice',3.99,'2021-01-25');
INSERT into shoppingcart.products values (4002,'Beverages','Coffee',3.99,'2021-01-25');
INSERT into shoppingcart.products values (4003,'Beverages','Tea',3.99,'2021-01-25');
INSERT into shoppingcart.products values (4004,'Beverages','Soda',3.99,'2021-01-25');
INSERT into shoppingcart.products values (4005,'Beverages','Water',3.99,'2021-01-25');
INSERT into shoppingcart.products values (5001,'Dairy','Milk',3.99,'2021-01-25');
INSERT into shoppingcart.products values (5002,'Dairy','Eggs',4.99,'2021-01-25');
INSERT into shoppingcart.products values (5003,'Dairy','Butter',3.99,'2021-01-25');
INSERT into shoppingcart.products values (5004,'Dairy','Cheese',3.99,'2021-01-25');
INSERT into shoppingcart.products values (5005,'Dairy','Yogurt',2.99,'2021-01-25');
INSERT into shoppingcart.products values (6001,'Condiments','Ketchup',3.99,'2021-01-25');
INSERT into shoppingcart.products values (6002,'Condiments','Ranch',4.99,'2021-01-25');
INSERT into shoppingcart.products values (6003,'Condiments','Honey',5.99,'2021-01-25');
INSERT into shoppingcart.products values (6004,'Condiments','Mayonnaise',3.99,'2021-01-25');
INSERT into shoppingcart.products values (6005,'Condiments','Pickles',3.99,'2021-01-25');


