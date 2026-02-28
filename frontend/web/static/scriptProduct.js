function getProductos() {
  fetch("http://192.168.100.3:5003/api/productos")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);

      var productListBody = document.querySelector("#product-list tbody");
      productListBody.innerHTML = "";

      data.forEach((producto) => {
        var row = document.createElement("tr");

        // Nombre
        var nombreCell = document.createElement("td");
        nombreCell.textContent = producto.nombre;
        row.appendChild(nombreCell);

        // Precio
        var precioCell = document.createElement("td");
        precioCell.textContent = producto.precio;
        row.appendChild(precioCell);

        // Stock
        var stockCell = document.createElement("td");
        stockCell.textContent = producto.stock;
        row.appendChild(stockCell);

        // Acciones
        var actionsCell = document.createElement("td");

        // Editar
        var editLink = document.createElement("a");
        editLink.href = `/editProducto/${producto.id}`;
        editLink.textContent = "Edit";
        editLink.className = "btn btn-primary mr-2";
        actionsCell.appendChild(editLink);

        // Eliminar
        var deleteLink = document.createElement("a");
        deleteLink.href = "#";
        deleteLink.textContent = "Delete";
        deleteLink.className = "btn btn-danger";
        deleteLink.addEventListener("click", function () {
          deleteProducto(producto.id);
        });
        actionsCell.appendChild(deleteLink);

        row.appendChild(actionsCell);
        productListBody.appendChild(row);
      });
    })
    .catch((error) => console.error("Error:", error));
}

function createProducto() {
  var data = {
    nombre: document.getElementById("nombre").value,
    precio: document.getElementById("precio").value,
    stock: document.getElementById("stock").value,
  };

  fetch("http://192.168.100.3:5003/api/productos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Producto creado:", data);
      getProductos(); // refresca la tabla
    })
    .catch((error) => console.error("Error:", error));
}

function updateProducto() {
  var productoId = document.getElementById("producto-id").value;

  var data = {
    nombre: document.getElementById("nombre").value,
    precio: document.getElementById("precio").value,
    stock: document.getElementById("stock").value,
  };

  fetch(`http://192.168.100.3:5003/api/productos/${productoId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Producto actualizado:", data);
    })
    .catch((error) => console.error("Error:", error));
}

function deleteProducto(productoId) {
  console.log("Deleting producto with ID:", productoId);

  if (confirm("Are you sure you want to delete this product?")) {
    fetch(`http://192.168.100.3:5003/api/productos/${productoId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Producto eliminado:", data);
        getProductos();
      })
      .catch((error) => console.error("Error:", error));
  }
}
