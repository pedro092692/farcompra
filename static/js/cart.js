const socket = io({autoConnect: false});

function update_cart_quantity(input){
    const new_quantity = parseInt(input.value);
    socket.connect();

    const item_id = input.getAttribute('row_id')
    socket.emit('update_cart_quantity', item_id, new_quantity)

    socket.on('update_cart', function(cart_item){
        let currentElement = input;
          while (currentElement && currentElement.tagName !== 'TABLE') {
            currentElement = currentElement.parentElement;
        }

       const table = currentElement;

        const td_total = table.querySelector('#total');
        const td_grand_total = table.querySelector('#grand-total');
        td_total.innerHTML = cart_item.total;
        td_grand_total.innerHTML = cart_item.grand_total;
    });
}

