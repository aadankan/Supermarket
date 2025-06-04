import React, { useState, useEffect } from "react";
import trashIcon from "../../assets/icons/trash.svg";
import editIcon from "../../assets/icons/edit.svg";

interface Supplier {
  id: number;
  name: string;
  email?: string;
  phone_number?: string;
}

const SuppliersTable = () => {
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [selectedSupplier, setSelectedSupplier] = useState<Supplier | null>(null);

  const fetchSuppliers = async () => {
    try {
      const response = await fetch("http://localhost:8000/suppliers", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) throw new Error("Failed to fetch suppliers");
      const data = await response.json();
      setSuppliers(data);
    } catch (error) {
      console.error("Error fetching suppliers:", error);
    }
  };

  useEffect(() => {
    fetchSuppliers();
  }, []);

  const handleEditClick = (supplier: Supplier) => {
    setSelectedSupplier(supplier);
    setIsEditModalOpen(true);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!selectedSupplier) return;
    const { name, value } = e.target;
    setSelectedSupplier((prev) => (prev ? { ...prev, [name]: value } : prev));
  };

  const handleSave = async () => {
    if (!selectedSupplier) return;

    // Walidacja minimalna
    if (!selectedSupplier.name.trim()) {
      alert("Nazwa dostawcy jest wymagana.");
      return;
    }

    try {
      if (selectedSupplier.id === 0) {
        // Dodawanie nowego dostawcy (POST)
        const response = await fetch("http://localhost:8000/suppliers", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            name: selectedSupplier.name,
            email: selectedSupplier.email,
            phone_number: selectedSupplier.phone_number,
          }),
        });

        if (!response.ok) throw new Error("Failed to add supplier");
        const newSupplier = await response.json();
        setSuppliers((prev) => [...prev, newSupplier]);
      } else {
        // Aktualizacja istniejącego dostawcy (PUT)
        const originalSupplier = suppliers.find((s) => s.id === selectedSupplier.id);
        const isUnchanged =
          originalSupplier?.name === selectedSupplier.name &&
          originalSupplier?.email === selectedSupplier.email &&
          originalSupplier?.phone_number === selectedSupplier.phone_number;

        if (isUnchanged) {
          setIsEditModalOpen(false);
          setSelectedSupplier(null);
          return;
        }

        const response = await fetch(`http://localhost:8000/suppliers/${selectedSupplier.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify(selectedSupplier),
        });

        if (!response.ok) throw new Error("Failed to update supplier");
        const updatedSupplier = await response.json();
        setSuppliers((prev) =>
          prev.map((s) => (s.id === updatedSupplier.id ? updatedSupplier : s))
        );
      }

      setIsEditModalOpen(false);
      setSelectedSupplier(null);
    } catch (error) {
      console.error("Error saving supplier:", error);
      alert("Nie udało się zapisać dostawcy. Spróbuj ponownie później.");
    }
  };

  return (
    <>
      <div className="w-full flex justify-between items-center">
        <p className="text-2xl mb-4 font-semibold">Selected Tab: Suppliers</p>
        <button
          className="px-4 py-1 mb-3 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors cursor-pointer shadow-md"
          onClick={() => {
            setSelectedSupplier({ id: 0, name: "", email: "", phone_number: "" });
            setIsEditModalOpen(true);
          }}
        >
          Dodaj dostawcę
        </button>
      </div>

      <div className="h-[88%] flex flex-col gap-2 overflow-auto relative">
        {/* Header */}
        <div className="w-full px-2 py-2 sticky top-0 bg-gray-200 rounded-lg shadow-sm flex justify-between items-center font-semibold text-gray-800">
          <p className="w-1/12">ID</p>
          <p className="w-3/12">Nazwa</p>
          <p className="w-4/12">Email</p>
          <p className="w-2/12">Phone number</p>
          <p className="w-1/12 text-center">Akcje</p>
        </div>

        {/* Supplier Rows */}
        {suppliers
          .sort((a, b) => a.id - b.id)
          .map((supplier) => (
            <div
              key={supplier.id}
              className="w-full px-2 py-2 bg-white rounded-lg shadow-md flex justify-between items-center"
            >
              <p className="w-1/12">{supplier.id}</p>
              <p className="w-3/12">{supplier.name}</p>
              <p className="w-4/12">{supplier.email}</p>
              <p className="w-2/12">{supplier.phone_number}</p>
              <div className="w-1/12 flex justify-center items-center gap-2">
                <div
                  className="cursor-pointer hover:bg-gray-200 p-1 rounded-full"
                  onClick={() => handleEditClick(supplier)}
                >
                  <img className="w-4" src={editIcon} alt="Edytuj" />
                </div>
              </div>
            </div>
          ))}
      </div>

      {/* Edit Modal */}
      {isEditModalOpen && selectedSupplier && (
        <div className="fixed inset-0 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-[400px] flex flex-col gap-4">
            <h2 className="text-lg font-bold">
              {selectedSupplier.id === 0 ? "Dodaj Dostawcę" : "Edytuj Dostawcę"}
            </h2>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Nazwa
              <input
                type="text"
                name="name"
                value={selectedSupplier.name}
                onChange={handleInputChange}
                className="border rounded px-2 py-1 mt-1"
              />
            </label>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Email
              <input
                type="email"
                name="email"
                value={selectedSupplier.email || ""}
                onChange={handleInputChange}
                className="border rounded px-2 py-1 mt-1"
              />
            </label>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Phone Number
              <input
                type="text"
                name="phone_number"
                value={selectedSupplier.phone_number || ""}
                onChange={handleInputChange}
                className="border rounded px-2 py-1 mt-1"
              />
            </label>

            <div className="flex justify-end gap-2 mt-4">
              <button
                onClick={() => {
                  setIsEditModalOpen(false);
                  setSelectedSupplier(null);
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

export default SuppliersTable;
