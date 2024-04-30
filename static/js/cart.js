const socket = io({autoConnect: false});

function update_cart_quantity(input){
    const new_quantity = parseInt(input.value);
    socket.connect();

    const item_id = input.getAttribute('row_id')
    socket.emit('update_cart_quantity', item_id, new_quantity)

    socket.on('update_cart', function(cart_item){
        const td_total = document.getElementById('total-'+cart_item.id);
        td_total.innerHTML = '$'+cart_item.total;
        const td_grand_total = document.getElementById('grand-total-'+cart_item.supplier);
        td_grand_total.innerHTML = '$'+cart_item.grand_total;
    });
}

function delete_cart_item(cart_item_id){
    socket.connect();
    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, delete it!"
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "Deleted!",
          text: "Your file has been deleted.",
          icon: "success"
        });
        socket.emit('delete_cart_item', cart_item_id)
      }
    });
}


