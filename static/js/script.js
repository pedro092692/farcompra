function toggleListItem(list) {
    let ul_prices = document.querySelectorAll('[id=prices]');
     for (const ulElement of ul_prices){
        ulElement.style.display = "none";
     }

    listItemElement = list.nextElementSibling;


  if (listItemElement.style.display === "none") {
    listItemElement.style.display = "block";
  } else {
    listItemElement.style.display = "none";
 }
}


const search_input = document.getElementById('search');
search_input.addEventListener('keyup', search);
search_input.addEventListener('change', search);
const socket = io({autoConnect: false});

function search(){
    socket.connect();
    socket.emit('search_query', search_input.value);

}

socket.on('search_results', function(data){
    const resultElement = document.getElementById('results')
    resultElement.innerHTML = ''

    data.results.forEach(function(result){
        const listItem = document.createElement('li');
        listItem.textContent = result.name;

        //Create sublist for prices
        const prices_ul = document.createElement('ul');
        prices_ul.setAttribute('id', 'prices')
        listItem.appendChild(prices_ul)


        result.prices.forEach(function(price){
            const prices_li = document.createElement('li');
            prices_li.textContent = price.supplier_name + ':';
            prices_li.appendChild(document.createElement('br'));
            prices_li.innerHTML += '$' + price.price + ' Vence ' + price.due_date + ' Stock ' + price.stock;
            prices_ul.appendChild(prices_li);

        })
        resultElement.appendChild(listItem);

        listItem.addEventListener('click', function(){
            alert('hi ')
            let ul_prices = document.querySelectorAll('[id=prices]');
            for (const ulElement of ul_prices){
                ulElement.style.display = "none";
            }
            prices_ul.style.display = 'block';
        });
    });
});




