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

function openAddTag(id) {
    document.getElementById("add-tag").style.display = "block";
    document.getElementById("add-tag-pid").value = id;
    console.log("here")
}

function closeAddTag() {
    document.getElementById("add-tag").style.display = "none";
}

window.onclick = function(event) {
    const addItem = this.document.getElementById("add-item")
    const addTag = this.document.getElementById("add-tag")
    if (event.target === addItem) {
        addItem.style.display = "none";
    }
    else if (event.target === addTag) {
        addTag.style.display = "none";
    }
}

window.addEventListener("beforeunload", function () {
    localStorage.setItem("scrollY", window.scrollY);
});

window.addEventListener("load", function () {
    const scrollY = localStorage.getItem("scrollY");
    if (scrollY !== null) {
        window.scrollTo(0, parseInt(scrollY));
    }
});