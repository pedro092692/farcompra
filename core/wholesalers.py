import os



wholesalers = {
       "drovencentro": {
        "url": "clientes.drovencentro.com",
        "user": os.environ.get('DROVENCENTRO_USER'),
        "password": os.environ.get('DROVENCENTRO_PASS'),
        "path": '/inventario',
        "file_name": 'inventario.txt',
        "name": "drovencentro",
        "csv": False,
        "has_header": False,
        "header": "product_id;name;price_usd;stock;barcode;due_date",
        "fix_barcode": False,
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
        "header":  "barcode;product_id;name;wholesale_price_ves;price_usd_reference;final_price_ves;price_usd;stock;\
laboratory;credit_days;percent_supplier;dicount_supplier;digital_discount;\
soon_payment_discount;discount_per_volume;min_amount_per_volume;discount_per_row;min_amount_per_row;rows;due_date",
        "fix_barcode": False,
        "supplier_id": 6,
        "price_dollar": True
    },
    "drocerca":{
        "url": "drocerca.proteoerp.org",
        "user": os.environ.get('DROCERCA_USER'),
        "password": os.environ.get('DROCERCA_PASS'),
        "path": '/',
        "file_name": 'inventario.txt',
        "name": "drocerca",
        "csv": True,
        "has_header": True,
        "header": 'product_id;barcode;name;stock_merida;stock;stock_oriente;\
brand;price_usd;price_ves_discount;group;due_date;active_ingredient;scale;discount_per_scale;bonus;bonus_amount',
        "fix_barcode": True,
        "supplier_id": 2,
        "price_dollar": False
    },
    "harissa": {
        "url": "vantecsolser.com",
        "user": os.environ.get('HARISSA_USER'),
        "password": os.environ.get('HARISSA_PASS'),
        "path": '/',
        "file_name": 'inventario.txt',
        "name": "harissa",
        "csv": True,
        "has_header": False,
        "header":  "product_id;name;product_code;product_group;barcode;price_no_tax;stock;\
stock_2;stock_2;stock_3;stock_4;regulated;unknown_1;unknown_2;unknown_3;unknown_4;unknown_5;laboratory;price_usd;due_date;unknown_6,",
        "fix_barcode": False,
        "supplier_id": 4,
        "price_dollar": True
    },
    "vital_clinic":{
        # "url": "drogueriavitalclinic.com.ve" old ftp server,
        "url": "195.35.33.28",
        "user": os.environ.get('VITAL_CLINIC_USER'),
        "password": os.environ.get('VITAL_CLINIC_PASS'),
        "path": '/Existencia',
        "file_name": 'inventario.txt',
        "name": "vital_clinic",
        "csv": True,
        "has_header": False,
        "header" : 'product_id;barcode;name;due_date;price_usd;unknown;price_usd_2;stock',
        "fix_barcode": False,
        "supplier_id": 1,
        "price_dollar": True
    },

    "dronena":{
        "url": "ftp.dronena.com",
        "user": os.environ.get('DRONENA_USER'),
        "password": os.environ.get('DRONENA_PASS'),
        "path": '/Maracay/5203',
        "file_name": 'inventario.txt',
        "name": "dronena",
        "csv": False,
        "has_header": True,
        "header": 'product_id;name;price_usd;stock;discount;pharmacy_profit;discount_2;package;package_discount;barcode;\
type;product_code;lot;due_date;regulated;cold_chain;discount_3;discount_4;original;unknown_1;unknown_2;unknown_3',
        "fix_barcode": False,
        "supplier_id": 3,
        "price_dollar": False,

    },

    "test_server": {
            "url": "",
            "user": "anonymous",
            "password": "",
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


    "joskar": {
        "url": "ftp.drogueriajoskar.com",
        "user": os.environ.get('JOSKAR_USER'),
        "password": os.environ.get('JOSKAR_PASS'),
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

    "insuaminca":{
        "url": "ftp.insuaminca.com.ve",
        "user": os.environ.get('INSUAMINCA_USER'),
        "password": os.environ.get('INSUAMINCA_PASS'),
        "path": '/Inventario',
        "file_name": 'inventario.txt',
        "name": "insuaminca",
        "csv": False,
        "has_header": False,
        "header":  "product_id;barcode;name;due_date;final_price;sale_percent;price_usd;stock",
        "fix_barcode": False,
        "supplier_id": 8,
        "price_dollar": True
    },

    "drolanca":{
        "url": "ftp.drolanca.com",
        "user": os.environ.get('DROLANCA_USER'),
        "password": os.environ.get('DROLANCA_PASS'),
        "path": '/INVENTARIO',
        "file_name": 'Inventario.txt',
        "name": "drolanca",
        "csv": False,
        "has_header": True,
        "header":  "product_id;barcode;name;id;laboratory;unknown_1;unknown_2;unknown_3;price_usd;stock;due_date;unknown_5;"
                   "unknown_6;unknown_7;unknown_8;unknown_9;unknown_10;unknown_11;unknown_12;unknown_13;unknown_14;"
                   "unknown_15;"
                   "unknown_16;unknown_17;unknown_18;unknown_19;unknown_20;unknown_21;unknown_22;unknown_23;"
                   "unknown_24;unknown_25;"
                   "unknown_26;unknown_27;unknown_28;unknown_29;unknown_30",
        "fix_barcode": True,
        "fix_stock": True,
        "supplier_id": 17,
        "price_dollar": False
    },

}