function show_product_info(li){

    const div_prices = document.querySelectorAll('[id=prices]');
    for (const div_price of div_prices){
        div_price.style.display = "none";
    }

    info_div = li.children[0];
    info_div.style.display = 'block';
}

//socketio

const socket = io({autoConnect: false});
socket.connect();

function get_products(form, product_price_id, supplier_id, stock, sp_name, product_name){
    error_field = form.querySelector('p')

    event.preventDefault();
    const quantity = parseInt(form.elements['quantity'].value);
    if(quantity >= 1 && quantity <= stock ){
        error_field.style.display = 'none';
        // Add product to the database
        socket.emit('add_to_cart', product_price_id, supplier_id, quantity);

        // update view cart
        // check if shopping cart is empty
        try{
            const shopping_list = document.getElementById('shopping_list');
            const all_li = shopping_list.children;
            const suppliers_on_list = []
            // get suppliers on the shopping cart
            for(const supplier_li of all_li){
                const supplier_id_in_list = parseInt(supplier_li.getAttribute('id'));
                suppliers_on_list.push(supplier_id_in_list);
            }
            if(suppliers_on_list.includes(supplier_id)){
                const supplier_li = document.getElementById(supplier_id.toString());
                //products ul
                const products_ul = supplier_li.children[0];
                const id_product_prices_list = Array.from(products_ul.children).map( item => parseInt(item.id));
                if(!id_product_prices_list.includes(product_price_id)){
                    const new_product_li = document.createElement('li');
                    new_product_li.classList.add('list-group-item', 'font-weight-normal');
                    new_product_li.setAttribute('id', product_price_id);
                    new_product_li.innerHTML = product_name;
                    // create span for quantity
                    const span_quantity = document.createElement('span');
                    span_quantity.classList.add('font-weight-bold');
                    span_quantity.innerHTML = ' * ';
                    new_product_li.appendChild(span_quantity);
                    // Create total quantity span
                    const span_total_quantity = document.createElement('span');
                    span_total_quantity.setAttribute('id', 'quantity');
                    span_total_quantity.innerHTML = form.elements['quantity'].value;
                    new_product_li.appendChild(span_total_quantity);
                    products_ul.appendChild(new_product_li);
                }else{
                    socket.on('update_quantity', function(data){
                        const new_quantity = data.quantity;
                        const product_li = document.getElementById(product_price_id);
                        const span_quantity = product_li.children['quantity'];
                        span_quantity.innerHTML = new_quantity;
                    });
                }
            }else{
                //add new supplier to the list
                new_supplier_li = document.createElement('li');
                new_supplier_li.classList.add('list-group-item', 'text-capitalize', 'font-weight-bold');
                new_supplier_li.setAttribute('id', supplier_id);
                new_supplier_li.innerHTML = sp_name + ':';
                shopping_list.appendChild(new_supplier_li);
                // add product
                const new_product_ul = document.createElement('ul');
                new_product_ul.classList.add('list-group', 'mt-2');
                const new_product_li = document.createElement('li');
                new_product_li.classList.add('list-group-item', 'font-weight-normal');
                new_product_li.innerHTML = product_name;
                // create span for quantity
                const span_quantity = document.createElement('span');
                span_quantity.classList.add('font-weight-bold');
                span_quantity.innerHTML = ' * ';
                new_product_li.appendChild(span_quantity);
                // Create total quantity span
                const span_total_quantity = document.createElement('span');
                span_total_quantity.setAttribute('id', 'quantity');
                span_total_quantity.innerHTML = form.elements['quantity'].value;
                new_product_li.appendChild(span_total_quantity);
                new_product_li.setAttribute('id', product_price_id);
                new_product_ul.appendChild(new_product_li);
                new_supplier_li.appendChild(new_product_ul);

            }
        }catch(TypeError){
            const cart_container = document.getElementById('cart_container');
            //reset content of the div
            cart_container.innerHTML = '';
            //create ul
            const ul = document.createElement('ul');
            ul.setAttribute('id', 'shopping_list');
            ul.classList.add('list-group');
            // Create li for supplier
            const li_supplier = document.createElement('li');
            li_supplier.classList.add('list-group-item', 'text-capitalize', 'font-weight-bold');
            li_supplier.setAttribute('id', supplier_id);
            li_supplier.innerHTML = sp_name + ':';
            // create ul products
            const ul_products = document.createElement('ul');
            ul_products.classList.add('list-group', 'mt-2');
            // create li product
            const li_product = document.createElement('li');
            li_product.classList.add('list-group-item', 'font-weight-normal');
            // add product name
            li_product.innerHTML = product_name;
            // create span for quantity
            const span_quantity = document.createElement('span');
            span_quantity.classList.add('font-weight-bold');
            span_quantity.innerHTML = ' * ';
            li_product.appendChild(span_quantity);
            // Create total quantity span
            const span_total_quantity = document.createElement('span');
            span_total_quantity.setAttribute('id', 'quantity');
            span_total_quantity.innerHTML = form.elements['quantity'].value;
            li_product.appendChild(span_total_quantity);
            li_product.setAttribute('id', product_price_id);
            // append li to ul products
            ul_products.appendChild(li_product);
            // append ul product to li supplier
            li_supplier.appendChild(ul_products);
            ul.appendChild(li_supplier);
            cart_container.appendChild(ul);
        }

    }else{
          error_field.style.display = 'block';
    }


}





