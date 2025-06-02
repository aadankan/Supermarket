import { useState } from "react";

interface ProductProps {
  product: {
    price: number | string;
    image_url: string;
    name: string;
    // add other product fields as needed
  };
  addToCart: (product: any, count: number) => void;
}

const Product = ({ product, addToCart }: ProductProps) => {
  const [count, setCount] = useState(1);

  const price = typeof product.price === "number" ? product.price : parseFloat(product.price);
  const fullPrice = (price * count).toFixed(2);

  return (
    <div className="w-32 bg-white outline-2 outline-blue-600 rounded-lg shadow-md p-3 flex flex-col items-center">
      <img src={product.image_url} alt={product.name} className="w-18 h-12 object-cover mb-2 rounded outline-2" />
      <h3 className="font-semibold text-black">{product.name}</h3>
      <div className="w-full flex items-center justify-center gap-1">
        <button
          className="w-8 h-8 bg-blue-100 rounded-full text-2xl cursor-pointer"
          onClick={() => setCount(count > 1 ? count - 1 : 1)}
        >
          -
        </button>
        <input
          type="number"
          min="1"
          max="99"
          value={count}
          onChange={(e) => {
            const value = parseInt(e.target.value, 10);
            if (!isNaN(value) && value >= 1 && value <= 99) {
              setCount(value);
            } else if (value >= 99) {
              setCount(99);
            } else {
              setCount(1);
            }
          }}
          className="w-8 h-8 p-1 text-center border border-blue-500 rounded-full"
        />
        <button
          className="w-8 h-8 bg-blue-100 rounded-full text-2xl cursor-pointer"
          onClick={() => setCount(count < 99 ? count + 1 : 99)}
        >
          +
        </button>
      </div>
      <p className="text-xs text-gray-700 font-bold mt-2">
        {fullPrice}$
      </p>
      <button onClick={() => addToCart(product, count)} className="p-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors cursor-pointer mt-1">
        Add to Cart
      </button>
    </div>
  );
};

export default Product;
