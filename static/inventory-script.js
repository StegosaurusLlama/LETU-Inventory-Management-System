function editItem(id) {
    const newName = prompt("Enter new item name:", document.getElementById('name-' + id).innerText);
    if (newName) {
        document.getElementById('name-' + id).innerText = newName;
    }
    const newDesc = prompt("Enter new description:", document.getElementById('desc-' + id).innerText);
    if (newDesc) {
        document.getElementById('desc-' + id).innerText = newDesc;
    }
}

function openAddItem() {
    document.getElementById("add-item").style.display = "block";
    console.log("here")
}

function closeAddItem() {
    document.getElementById("add-item").style.display = "none";
}

window.onclick = function(event) {
    const addItem = this.document.getElementById("add-item")
    if (event.target === addItem) {
        addItem.style.display = "none";
    }
}