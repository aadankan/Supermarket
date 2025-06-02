import React, { useState, useEffect } from "react";
import trashIcon from "../../assets/icons/trash.svg";
import editIcon from "../../assets/icons/edit.svg";



interface Category {
  id: number;
  name: string;
}

const CategoriesTable = () => {
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(null);

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
    fetchCategories();
  }, [selectedCategory]);

  const handleEditClick = (category: Category) => {
    setSelectedCategory(category);
    setIsEditModalOpen(true);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!selectedCategory) return;
    const { name, value } = e.target;
    setSelectedCategory({
      ...selectedCategory,
      [name]: value,
    });
  };

  const handleSave = async () => {
    if (!selectedCategory) return;
    const originalCategory = categories.find((c) => c.id === selectedCategory.id);
    if (selectedCategory === originalCategory) {
      setIsEditModalOpen(false);
      setSelectedCategory(null);
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/categories/${selectedCategory.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(selectedCategory),
      });

      if (!response.ok) throw new Error("Failed to update category");
      const updatedCategory = await response.json();
      setCategories((prev) => prev.map((c) => (c.id === updatedCategory.id ? updatedCategory : c)));
    } catch (error) {
      console.error("Error updating product:", error);
      alert("Failed to update product. Please try again later.");
    }

    setIsEditModalOpen(false);
    setSelectedCategory(null);
  };

  return (
    <>
      <div className="h-[88%] flex flex-col gap-2 overflow-auto relative">
        {/* Header */}
        <div className="w-full px-2 py-2 sticky top-0 bg-gray-200 rounded-lg shadow-sm flex justify-between items-center font-semibold text-gray-800">
          <p className="w-1/12">ID</p>
          <p className="w-4/12">Nazwa</p>
          <p className="w-1/12 text-center">Akcje</p>
        </div>

        {/* Category Rows */}
        {[...categories]
          .sort((a, b) => a.id - b.id)
          .map((category) => (
            <div
              key={category.id}
              className="w-full px-2 py-2 bg-white rounded-lg shadow-md flex justify-between items-center"
            >
              <p className="w-1/12">{category.id}</p>
              <p className="w-4/12">{category.name}</p>
              <div className="w-1/12 flex justify-center items-center gap-2">
                <div
                  className="cursor-pointer hover:bg-gray-200 p-1 rounded-full"
                  onClick={() => handleEditClick(category)}
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
      {isEditModalOpen && selectedCategory && (
        <div className="fixed inset-0 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-[400px] flex flex-col gap-4">
            <h2 className="text-lg font-bold">Edytuj produkt</h2>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Nazwa
              <input
                type="text"
                name="name"
                value={selectedCategory.name}
                onChange={handleInputChange}
                className="border rounded px-2 py-1 mt-1"
              />
            </label>

            <div className="flex justify-end gap-2 mt-4">
              <button
                onClick={() => {
                  setIsEditModalOpen(false);
                  setSelectedCategory(null);
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

export default CategoriesTable;
