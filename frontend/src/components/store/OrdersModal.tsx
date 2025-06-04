import React, { useState } from "react";

type OrderItem = {
  id: number;
  order_date: string;
  status: string;
  items: {
    product_id: number;
    quantity: number;
    price: string;
    name: string;
    image_url: string;
  }[];
};

type OrdersModalProps = {
  orders: OrderItem[];
  onClose: () => void;
};

const OrdersModal: React.FC<OrdersModalProps> = ({ orders, onClose }) => {
  const [expandedOrders, setExpandedOrders] = useState<number[]>([]);

  const toggleExpand = (orderId: number) => {
    setExpandedOrders((prev) =>
      prev.includes(orderId)
        ? prev.filter((id) => id !== orderId)
        : [...prev, orderId]
    );
  };

  return (
    <div className="fixed inset-0 flex justify-center items-center z-50">
      <div className="bg-white rounded-lg shadow-lg max-w-lg w-full max-h-[80vh] overflow-auto p-6">
        <h2 className="text-2xl font-bold mb-4">Twoje zamówienia</h2>
        {orders.length === 0 ? (
          <p>Brak zamówień.</p>
        ) : (
          <ul className="space-y-4">
            {orders.map((order) => {
              const isExpanded = expandedOrders.includes(order.id);
              const totalPrice = order.items.reduce(
                (sum, item) => sum + Number(item.price) * item.quantity,
                0
              );
              return (
                <li key={order.id} className="border p-3 rounded-md">
                  <p>
                    <strong>ID:</strong> {order.id}
                  </p>
                  <p>
                    <strong>Data:</strong>{" "}
                    {new Date(order.order_date).toLocaleString()}
                  </p>
                  <p>
                    <strong>Status:</strong> {order.status}
                  </p>
                  <p>
                    <strong>Łączna cena:</strong> {totalPrice.toFixed(2)} zł
                  </p>

                  <button
                    onClick={() => toggleExpand(order.id)}
                    className="mt-2 text-blue-600 hover:underline cursor-pointer"
                  >
                    {isExpanded ? "Ukryj produkty" : "Pokaż produkty"}
                  </button>

                  {isExpanded && (
                    <ul className="mt-2 space-y-2">
                      {order.items.map((item, index) => (
                        <li
                          key={index}
                          className="flex items-center gap-3 border rounded p-2"
                        >
                          <img
                            src={item.image_url}
                            alt={item.name}
                            className="w-12 h-12 object-cover rounded"
                          />
                          <div>
                            <p className="font-medium">{item.name}</p>
                            <p>
                              Ilość: {item.quantity}, Cena: {item.price} zł
                            </p>
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}
                </li>
              );
            })}
          </ul>
        )}
        <button
          onClick={onClose}
          className="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 cursor-pointer transition-colors"
        >
          Zamknij
        </button>
      </div>
    </div>
  );
};

export default OrdersModal;
