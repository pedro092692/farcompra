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
      title: "¿Estás seguro?",
      text: "¡No podrás revertir esto!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "¡Sí, bórralo!"
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "¡Eliminado!",
          text: "Su registro ha sido eliminado.",
          icon: "success"
        });
        socket.emit('delete_cart_item', cart_item_id)
        setTimeout(function(){
            location.reload();
        }, 1800);

      }
    });
}


function delete_cart_all(supplier_id){
    socket.connect();
    Swal.fire({
      title: "¿Estás seguro?",
      text: "¡No podrás revertir esto!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "¡Sí, bórralo!"
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "¡Eliminado!",
          text: "Su Carrito ha sido eliminado.",
          icon: "success"
        });
        socket.emit('delete_cart_all', supplier_id)
        setTimeout(function(){
            location.reload();
        }, 1800);

      }
    });
}

function checkout_supplier(supplier){
    event.preventDefault();
    let form = document.getElementById('form-'+supplier);
    let container_div = document.querySelector("[supplier='"+supplier+"']");
    let main_div = document.getElementById('main-col');

    container_div.style.display = 'none';

    let = hidden_suppliers = []
    for(item in main_div.children){
       let display_style = main_div.children[item];
       try{
            let style = main_div.children[item].style.display
            if(style === ''){
                style = 'block';
            }

            hidden_suppliers.push(style);

       }catch(TypeError){
       }
    }
    if(! hidden_suppliers.includes('block')){
        let p = document.createElement('p')
        p.classList.add('text-center', 'text-md', 'mt-2', 'font-weight-bold')
        p.innerHTML = 'Your Cart is empty.';
        main_div.appendChild(p);
    }


    form.submit();


}

function checkout_supplier_excel(supplier){
    event.preventDefault();
    let form = document.getElementById('form-'+supplier+'-excel');
    let container_div = document.querySelector("[supplier='"+supplier+"']");
    let main_div = document.getElementById('main-col');

    container_div.style.display = 'none';

    let = hidden_suppliers = []
    for(item in main_div.children){
       let display_style = main_div.children[item];
       try{
            let style = main_div.children[item].style.display
            if(style === ''){
                style = 'block';
            }

            hidden_suppliers.push(style);

       }catch(TypeError){
       }
    }
    if(! hidden_suppliers.includes('block')){
        let p = document.createElement('p')
        p.classList.add('text-center', 'text-md', 'mt-2', 'font-weight-bold')
        p.innerHTML = 'Your Cart is empty.';
        main_div.appendChild(p);
    }


    form.submit();

}





