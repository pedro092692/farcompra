const socket = io({autoConnect: false});

function update_supplier_discount(supplier_id, discount_name){
    socket.connect();
    let discount = document.getElementById(discount_name).value;
    socket.emit('update_discount', supplier_id, discount)

}