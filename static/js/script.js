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



