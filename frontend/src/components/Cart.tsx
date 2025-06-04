type Props = {
  cartItems: {
    product: { id: number; name: string; price: number };
    count: number;
  }[];
  onClose: () => void;
  onRemove: (id: number) => void;
  onUpdateCount: (id: number, count: number) => void;
  onOrder: () => void; // <- nowy props
};

const CartModal: React.FC<Props> = ({
  cartItems,
  onClose,
  onRemove,
  onUpdateCount,
  onOrder,
}) => {
  const total = cartItems.reduce(
    (sum, item) => sum + item.product.price * item.count,
    0
  );

  return (
    <div className="fixed inset-0 bg-black/50 flex justify-center items-center z-50">
      <div className="bg-white w-[90%] max-w-md p-6 rounded-xl shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-3 right-4 text-2xl font-bold text-gray-600 hover:text-red-500 cursor-pointer"
        >
          &times;
        </button>
        <h2 className="text-2xl font-bold text-blue-700 mb-4">Twój koszyk</h2>
        {cartItems.length > 0 ? (
          <div className="flex flex-col gap-4 max-h-[300px] overflow-y-auto">
            {cartItems.map((item) => (
              <div
                key={item.product.id}
                className="border-b pb-2 flex justify-between items-start"
              >
                <div>
                  <h3 className="font-semibold">{item.product.name}</h3>
                  <p className="text-sm text-gray-600">
                    Cena: {item.product.price} zł
                  </p>
                  <div className="flex items-center gap-2 mt-1">
                    <button
                      onClick={() =>
                        onUpdateCount(item.product.id, item.count - 1)
                      }
                      className="px-2 bg-gray-200 rounded"
                    >
                      -
                    </button>
                    <span>{item.count}</span>
                    <button
                      onClick={() =>
                        onUpdateCount(item.product.id, item.count + 1)
                      }
                      className="px-2 bg-gray-200 rounded"
                    >
                      +
                    </button>
                  </div>
                </div>
                <button
                  onClick={() => onRemove(item.product.id)}
                  className="text-red-500 text-lg font-bold"
                >
                  ×
                </button>
              </div>
            ))}
            <div className="text-right font-bold mt-4">
              Suma: {total.toFixed(2)} zł
            </div>
            <button
              onClick={onOrder}
              className="mt-4 px-4 py-2 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition cursor-pointer"
            >
              Zamów teraz
            </button>
          </div>
        ) : (
          <p className="text-gray-500">Koszyk jest pusty.</p>
        )}
      </div>
    </div>
  );
};

export default CartModal;
