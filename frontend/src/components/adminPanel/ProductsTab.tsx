import React, { useState, useEffect } from "react";
import trashIcon from "../../assets/icons/trash.svg";
import editIcon from "../../assets/icons/edit.svg";

interface Product {
  id: number;
  name: string;
  price: number;
  image_url: string;
  description: string;
  category_id: number;
  inventory_quantity?: number;
}

interface Category {
  id: number;
  name: string;
}

const ProductTable = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);

  const fetchProducts = async () => {
    try {
      const response = await fetch("http://localhost:8000/products/full", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) throw new Error("Failed to fetch products");
      const data = await response.json();
      const mapped = data.map((p: any) => ({
        ...p,
        category_id: p.category_id || null,
      }));
      setProducts(mapped);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch("http://localhost:8000/categories", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) throw new Error("Failed to fetch categories");
      const data = await response.json();
      setCategories(data);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, [selectedProduct]);

  const handleEditClick = (product: Product) => {
    setSelectedProduct(product);
    setIsEditModalOpen(true);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!selectedProduct) return;
    const { name, value } = e.target;
    setSelectedProduct({
      ...selectedProduct,
      [name]: name === "price" || name === "inventory_quantity" ? Number(value) : value,
    });
  };

  const handleSave = async () => {
    if (!selectedProduct) return;
    const originalProduct = products.find((p) => p.id === selectedProduct.id);
    if (selectedProduct === originalProduct) {
      setIsEditModalOpen(false);
      setSelectedProduct(null);
      return;
    }

    if (selectedProduct?.inventory_quantity !== originalProduct?.inventory_quantity) {
      try {
        const response = await fetch(`http://localhost:8000/inventory/${selectedProduct.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            quantity: selectedProduct.inventory_quantity,
          }),
        });
        if (!response.ok) throw new Error("Failed to update inventory");
        await response.json();
      } catch (error) {
        console.error("Error updating inventory:", error);
        alert("Failed to update inventory. Please try again later.");
        return;
      }
      console.log("Inventory updated successfully");
    }
    try {
      const response = await fetch(`http://localhost:8000/products/${selectedProduct.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(selectedProduct),
      });

      if (!response.ok) throw new Error("Failed to update product");
      const updatedProduct = await response.json();
      setProducts((prev) => prev.map((p) => (p.id === updatedProduct.id ? updatedProduct : p)));
    } catch (error) {
      console.error("Error updating product:", error);
      alert("Failed to update product. Please try again later.");
    }

    setIsEditModalOpen(false);
    setSelectedProduct(null);
  };

  return (
    <>
      <div className="h-[88%] flex flex-col gap-2 overflow-auto relative">
        {/* Header */}
        <div className="w-full px-2 py-2 sticky top-0 bg-gray-200 rounded-lg shadow-sm flex justify-between items-center font-semibold text-gray-800">
          <p className="w-1/12">ID</p>
          <p className="w-4/12">Nazwa</p>
          <p className="w-1/12">Cena</p>
          <p className="w-2/12">Kategoria</p>
          <p className="w-1/12">Ilość</p>
          <p className="w-1/12 text-center">Akcje</p>
        </div>

        {/* Product Rows */}
        {[...products]
          .sort((a, b) => a.id - b.id)
          .map((product) => (
            <div
              key={product.id}
              className="w-full px-2 py-2 bg-white rounded-lg shadow-md flex justify-between items-center"
            >
              <p className="w-1/12">{product.id}</p>
              <p className="w-4/12">{product.name}</p>
              <p className="w-1/12">${product.price}</p>
              <p className="w-2/12">{categories.find((cat) => cat.id === product.category_id)?.name || "N/A"}</p>
              <p className="w-1/12">{product.inventory_quantity || "N/A"}</p>
              <div className="w-1/12 flex justify-center items-center gap-2">
                <div
                  className="cursor-pointer hover:bg-gray-200 p-1 rounded-full"
                  onClick={() => handleEditClick(product)}
                >
                  <img className="w-4" src={editIcon} alt="Edytuj" />
                </div>
                <div className="cursor-pointer hover:bg-gray-200 p-1 rounded-full">
                  <img className="w-4" src={trashIcon} alt="Usuń" />
                </div>
              </div>
            </div>
          ))}
      </div>
      {/* Edit Modal */}
      {isEditModalOpen && selectedProduct && (
        <div className="fixed inset-0 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-[400px] flex flex-col gap-4">
            <h2 className="text-lg font-bold">Edytuj produkt</h2>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Nazwa
              <input
                type="text"
                name="name"
                value={selectedProduct.name}
                onChange={handleInputChange}
                className="border rounded px-2 py-1 mt-1"
              />
            </label>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Cena
              <input
                type="number"
                name="price"
                value={selectedProduct.price}
                onChange={handleInputChange}
                className="border rounded px-2 py-1 mt-1"
              />
            </label>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Zdjęcie URL
              <input
                type="text"
                name="image_url"
                value={selectedProduct.image_url}
                onChange={handleInputChange}
                className="border rounded px-2 py-1 mt-1"
              />
            </label>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Opis
              <input
                type="text"
                name="description"
                value={selectedProduct.description || ""}
                onChange={handleInputChange}
                className="border rounded px-2 py-1 mt-1"
              />
            </label>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Kategoria
              <select
                name="category_id"
                value={selectedProduct.category_id || ""}
                onChange={(e) =>
                  setSelectedProduct((prev) => (prev ? { ...prev, category_id: Number(e.target.value) } : prev))
                }
                className="border rounded px-2 py-1 mt-1"
              >
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.name}
                  </option>
                ))}
              </select>
            </label>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Ilość
              <input
                type="number"
                name="inventory_quantity"
                value={selectedProduct.inventory_quantity || 0}
                onChange={handleInputChange}
                className="border rounded px-2 py-1 mt-1"
              />
            </label>

            <div className="flex justify-end gap-2 mt-4">
              <button
                onClick={() => {
                  setIsEditModalOpen(false);
                  setSelectedProduct(null);
                }}
                className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400 cursor-pointer"
              >
                Anuluj
              </button>
              <button
                onClick={handleSave}
                className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 cursor-pointer"
              >
                Zapisz
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ProductTable;
