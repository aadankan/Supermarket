import React, { useEffect, useState } from "react";
import editIcon from "../../assets/icons/edit.svg";

type Order = {
  id: number;
  user_id: number;
  order_date: string;
  status: string;
};

const OrdersTable = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  const fetchOrders = async () => {
    try {
      const response = await fetch("http://localhost:8000/orders", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) throw new Error("Failed to fetch orders");
      const data = await response.json();
      setOrders(data);
    } catch (error) {
      console.error("Error fetching orders:", error);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleEditClick = (order: Order) => {
    setSelectedOrder(order);
    setIsEditModalOpen(true);
  };

  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (!selectedOrder) return;
    setSelectedOrder({ ...selectedOrder, status: e.target.value });
  };

  const handleSave = async () => {
    if (!selectedOrder) return;

    try {
      const response = await fetch(`http://localhost:8000/orders/${selectedOrder.id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({ status: selectedOrder.status }),
      });

      if (!response.ok) throw new Error("Failed to update order");

      setOrders((prev) => prev.map((o) => (o.id === selectedOrder.id ? { ...o, status: selectedOrder.status } : o)));
      setIsEditModalOpen(false);
      setSelectedOrder(null);
    } catch (error) {
      console.error("Error updating order:", error);
      alert("Błąd podczas aktualizacji zamówienia.");
    }
  };

  return (
    <>
      <div className="w-full flex justify-between items-center">
        <p className="text-2xl mb-4 font-semibold">Selected Tab: Orders</p>
      </div>

      <div className="h-[88%] flex flex-col gap-2 overflow-auto relative">
        <div className="w-full px-2 py-2 sticky top-0 bg-gray-200 rounded-lg shadow-sm flex justify-between items-center font-semibold text-gray-800">
          <p className="w-1/12">ID</p>
          <p className="w-2/12">Użytkownik</p>
          <p className="w-4/12">Data</p>
          <p className="w-3/12">Status</p>
          <p className="w-1/12 text-center">Akcje</p>
        </div>

        {orders.map((order) => (
          <div
            key={order.id}
            className="w-full px-2 py-2 bg-white rounded-lg shadow-md flex justify-between items-center"
          >
            <p className="w-1/12">{order.id}</p>
            <p className="w-2/12">{order.user_id}</p>
            <p className="w-4/12">{new Date(order.order_date).toLocaleString()}</p>
            <p className="w-3/12 capitalize">{order.status}</p>
            <div className="w-1/12 flex justify-center items-center gap-2">
              <div className="cursor-pointer hover:bg-gray-200 p-1 rounded-full" onClick={() => handleEditClick(order)}>
                <img className="w-4" src={editIcon} alt="Edytuj" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal edycji statusu zamówienia */}
      {isEditModalOpen && selectedOrder && (
        <div className="fixed inset-0 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-[400px] flex flex-col gap-4">
            <h2 className="text-lg font-bold">Edytuj status zamówienia</h2>

            <label className="flex flex-col text-sm font-medium text-gray-700">
              Status
              <select
                value={selectedOrder.status}
                onChange={handleStatusChange}
                className="border rounded px-2 py-1 mt-1"
              >
                <option value="pending">Oczekujące</option>
                <option value="shipped">Wysłane</option>
                <option value="delivered">Dostarczone</option>
                <option value="cancelled">Anulowane</option>
              </select>
            </label>

            <div className="flex justify-end gap-2 mt-4">
              <button
                onClick={() => {
                  setIsEditModalOpen(false);
                  setSelectedOrder(null);
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

export default OrdersTable;
