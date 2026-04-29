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

// document.querySelectorAll(".edit-item-form").forEach(form => {
//   form.addEventListener("submit", async (e) => {
//     e.preventDefault();

//     const res = await fetch(form.action, {
//       method: form.method,
//       body: new FormData(form)
//     });

//     const data = await res.json();
//     const desc = document.getElementById("description-" + data["productID"]);
//     desc.textContent = "Description: " + data["desc"];
//     const modal = bootstrap.Modal.getInstance(document.getElementById("item-modal-" + data["productID"]));
//     modal.hide();
//   });
// });

document.querySelectorAll(".edit-stock-form").forEach(form => {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const res = await fetch(form.action, {
      method: form.method,
      body: new FormData(form)
    });

    const data = await res.json();
    const text = document.getElementById("stock-" + data["productID"]);
    const back = document.getElementById("stock-backdrop-" + data["productID"]);
    const overlay = document.getElementById("img-overlay-" + data["productID"]);
    const quantityField = document.getElementById("quantity-field-" + data["productID"]);

    quantityField.value = data["quantity"]

    if (data["stocked"] == 0) {
      text.textContent = "Out of stock";
      text.style = "color: #E44242";
      back.style.backgroundColor = "#E44242";
      overlay.style.display = "block";
    }
    else if (data["stocked"] == 1) {
      text.textContent = "Stock low";
      text.style = "color: #FFAA0C";
      back.style.backgroundColor = "#FFAA0C";
      overlay.style.display = "none";
    }
    else {
      text.style.display = "none";
      back.style.backgroundColor = "#ffffff";
      overlay.style.display = "none";
    }
    const desc = document.getElementById("description-" + data["productID"]);
    const modal = bootstrap.Modal.getInstance(document.getElementById("stock-modal-" + data["productID"]));
    modal.hide();
  });
});

document.querySelectorAll(".edit-tag-form").forEach(form => {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const res = await fetch(form.action, {
      method: form.method,
      body: new FormData(form)
    });

    const data = await res.json();
    const desc = document.getElementById("description-" + data["productID"]);
    desc.textContent = "Description: " + data["desc"];
    const modal = bootstrap.Modal.getInstance(document.getElementById("tag-modal-" + data["productID"]));
    modal.hide();
  });
});


window.onclick = function (event) {
  const addItem = this.document.getElementById("add-item")
  const addTag = this.document.getElementById("add-tag")
  if (event.target === addItem) {
    addItem.style.display = "none";
  }
  else if (event.target === addTag) {
    addTag.style.display = "none";
  }
}