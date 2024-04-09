wholesalers = {
    "vital_clinic":{
        "url": "drogueriavitalclinic.com.ve",
        "user": "cliente@drogueriavitalclinic.com.ve",
        "password": "2P0-3/+5WrbB",
        "path": '/Existencia',
        "file_name": 'inventario.txt',
        "name": "vital_clinic",
        "csv": True,
        "has_header": False,
        "header" : 'id;barcode;name;due_date;price_usd;unknown;price_usd_2;stock',
        "fix_barcode": False,
        "supplier_id": 1,
        "price_dollar": True
    },

    "drocerca":{
        "url": "drocerca.proteoerp.org",
        "user": "C00VV1",
        "password": "U*b7xGLT",
        "path": '/',
        "file_name": 'inventario.txt',
        "name": "drocerca",
        "csv": True,
        "has_header": True,
        "header": 'id;barcode;name;stock_merida;stock;stock_oriente;\
brand;price_usd;price_ves_discount;group;due_date;active_ingredient;scale;discount_per_scale;bonus;bonus_amount',
        "fix_barcode": True,
        "supplier_id": 2,
        "price_dollar": False
    },

    "dronena":{
        "url": "ftp.dronena.com",
        "user": "0491-foraneo",
        "password": "6luc2ztd",
        "path": '/Clientes/0491',
        "file_name": 'inventario.txt',
        "name": "dronena",
        "csv": False,
        "has_header": True,
        "header": 'id;name;price_usd;stock;discount;pharmacy_profit;discount_2;package;package_discount;barcode;\
type;product_code;lot;due_date;regulated;cold_chain;discount_3;discount_4;original;unknown_1;unknown_2;unknown_3',
        "fix_barcode": False,
        "supplier_id": 3,
        "price_dollar": False

    },

    "harissa": {
        "url": "vantecsolser.com",
        "user": "harissa@vantecsolser.com",
        "password": "t6tUlAzrG!Js",
        "path": '/',
        "file_name": 'inventario.txt',
        "name": "harissa",
        "csv": True,
        "has_header": False,
        "header":  "0;name;product_code;product_group;barcode;price_no_tax;stock;\
stock_2;stock_2;stock_3;stock_4;regulated;unknown_1;unknown_2;unknown_3;unknown_4;unknown_5;laboratory;price_usd;due_date",
        "fix_barcode": False,
        "supplier_id": 4,
        "price_dollar": True
    },

    "test_server": {
            "url": "",
            "user": "anonymous",
            "password": "pedro",
            "path": '/data',
            "file_name": 'inventario.txt',
            "name": "test_server",
            "fix_data": False,
            "fix_header": True,
            "header":  "id;product_info;row_1;medicine_type;barcode;price;stock;row_2;row_3;row_4;row_5;row_6;row_7;row_8;row_9;row_10;row_11;laboratory;price_usd",
            "headers": ['medicine_type', 'id'],
            "fix_barcode": False,
            "database_headers": ['medicine_type', 'barcode', 'row_5', 'price'],
            "supplier_id": 10,
            "price_dollar": False
        },

    "droven_centro": {
        "url": "clientes.drovencentro.com",
        "user": "F600249",
        "password": "Clientes1234",
        "path": '',
        "file_name": 'inventario.txt',
        "name": "droven_centro",
        "header":  "id;product_info;row_1;medicine_type;barcode;price;stock;row_2;row_3;row_4;row_5;row_6;row_7;row_8;row_9;row_10;row_11;laboratory;price_usd",
        "headers": ['medicine_type', 'id'],
        "fix_barcode": False,
        "database_headers": ['medicine_type', 'barcode', 'row_5', 'price'],
        "supplier_id": 5,
        "price_dollar": False
    },


    "cobeca": {
        "url": "",
        "user": "",
        "password": "",
        "path": '',
        "file_name": 'cobeca.xlsx',
        "name": "cobeca",
        "csv": False,
        "has_header": True,
        "header":  "barcode;id;name;wholesale_price_ves;price_usd_reference;final_price_ves;price_usd;stock;\
laboratory;credit_days;percent_supplier;dicount_supplier;digital_discount;\
soon_payment_discount;discount_per_volume;min_amount_per_volume;discount_per_row;min_amount_per_row;rows;due_date",
        "fix_barcode": False,
        "supplier_id": 6,
        "price_dollar": True
    },

    "joskar": {
        "url": "ftp.drogueriajoskar.com",
        "user": "u551098694.invftp02",
        "password": "mayorFTP01",
        "path": '/catalogo',
        "file_name": 'catalogo_mayor.txt',
        "name": "joskar",
        "csv": True,
        "has_header": True,
        "header":  "barcode;name;price_usd;sale;due_date;stock",
        "fix_barcode": False,
        "supplier_id": 7,
        "price_dollar": True
    },



}