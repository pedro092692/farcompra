wholesalers = {
    "vital_clinic":{
        "url": "drogueriavitalclinic.com.ve",
        "user": "cliente@drogueriavitalclinic.com.ve",
        "password": "2P0-3/+5WrbB",
        "path": '/Existencia',
        "file_name": 'inventario.txt',
        "name": "vital_clinic",
        "csv": True,
        "header" : 'id;barcode;product_info;due_date;price;unknown;price_2;stock',
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
        "header": [],
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
        "header": [],
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
        "header":  "id;product_info;row_1;medicine_type;barcode;price;stock;row_2;row_3;row_4;row_5;row_6;row_7;row_8;row_9;row_10;row_11;laboratory;price_usd",
        "supplier_id": 4,
        "price_dollar": True
    },

    "test_server": {
            "url": "127.0.0.1",
            "user": "anonymous",
            "password": "pedro",
            "path": '/',
            "file_name": 'inventario.txt',
            "name": "test_server",
            "fix_data": False,
            "fix_header": True,
            "header":  "id;product_info;row_1;medicine_type;barcode;price;stock;row_2;row_3;row_4;row_5;row_6;row_7;row_8;row_9;row_10;row_11;laboratory;price_usd",
            "headers": ['medicine_type', 'id'],
            "fix_barcode": False,
            "database_headers": ['medicine_type', 'barcode', 'row_5', 'price'],
            "supplier_id": 5,
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
}