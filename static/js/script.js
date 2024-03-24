function toggleListItem(list) {
    listItemElement = list.nextElementSibling;
  if (listItemElement.style.display === "none") {
    listItemElement.style.display = "block";
  } else {
    listItemElement.style.display = "none";
 }
}



