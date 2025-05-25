import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import supermarketInside from "../assets/images/SupermarketInside.png";
import AdminPanel from "../components/account.tsx/AdminPanel";
import exit from "../assets/icons/exit.svg";
import filter from "../assets/icons/filter.svg";
import cart from "../assets/icons/cart.svg";
import search from "../assets/icons/search.svg";

const Store = () => {
  const [filterActive, setFilterActive] = useState(false);
  const [cartActive, setCartActive] = useState(false);
  const [searchActive, setSearchActive] = useState(false);
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);

  const navigate = useNavigate();

  const adminPanel = () => {
    navigate("/admin");
  };

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const getProducts = async () => {
    try {
      const response = await fetch("http://localhost:8000/products", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      return await response.json();
    } catch (error) {
      console.error("Error fetching products:", error);
      alert("Failed to fetch products. Please try again later.");
    }
  };

  const getCatergories = async () => {
    try {
      const response = await fetch("http://localhost:8000/categories", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      return await response.json();
    } catch (error) {
      console.error("Error fetching categories:", error);
      alert("Failed to fetch categories. Please try again later.");
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      const productsData = await getProducts();
      const categoriesData = await getCatergories();
      setProducts(productsData);
      setCategories(categoriesData);
    };

    fetchData();
  }, []);

  return (
    <div
      style={{ backgroundImage: `url(${supermarketInside})` }}
      className="w-screen h-screen bg-cover bg-center flex flex-col items-center justify-center gap-[5%]"
    >
      <div className="w-[80%] h-[10%] flex items-center justify-between gap-4">
        <div
          style={{
            WebkitTextStrokeWidth: "0.2px",
            WebkitTextStrokeColor: "#000",
          }}
          className="w-fit p-4 rounded-2xl bg-amber-400 text-blue-800 text-5xl font-normal font-['Jacques_Francois_Shadow'] [text-shadow:_2px_2px_5px_rgb(0_0_0_/_1)]"
        >
          Supermarket
        </div>
        <div className="w-auto flex items-center justify-between gap-4">
          <AdminPanel adminPanel={adminPanel} />
          <div className="w-[64px] h-16 relative bg-blue-600 rounded-2xl overflow-hidden cursor-pointer">
            <img src={exit} alt="Exit" className="p-2" onClick={logout} />
          </div>
        </div>
      </div>
      <div className="w-[80%] h-[80%] bg-white/80 p-8 rounded-xl shadow-lg flex flex-col items-center justify-start gap-4 overflow-hidden">
        <div className="w-full flex items-center justify-between px-4">
          <div>
            <h1 className="text-4xl font-bold text-blue-600 font-['Jacques_Francois_Shadow']">Welcome to the Store!</h1>
          </div>
          <div className="flex items-center justify-end gap-8">
            <img src={filter} alt="Filter" className="w-8 h-8 cursor-pointer" />
            <img src={search} alt="Search" className="w-8 h-8 cursor-pointer" />
            <img src={cart} alt="Cart" className="w-8 h-8 cursor-pointer mb-1" />
          </div>
        </div>
        <div className="w-full flex items-center justify-center bg-blue-200/50 outline-2 outline-blue-500 rounded-xl">
          {categories.length > 0 ? (
            <div className="flex justify-center items-center gap-4 overflow-auto">
              {categories.map((category) => (
                <div
                  key={category.id}
                  className="m-2 px-4 py-2 bg-blue-700 rounded-full shadow-md outline-3 outline-blue-500 cursor-pointer"
                >
                  <h2 className="text-xl font-semibold text-white text-center">{category.name}</h2>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No categories available.</p>
          )}
        </div>
        <div className="w-full flex flex-wrap justify-center items-center gap-6 mt-4">
          {products.length > 0 ? (
            products.map((product) => (
              <div
                key={product.id}
                className="w-[100px] h-[150px] bg-white rounded-lg shadow-md p-4 flex flex-col items-center"
              >
                <img src={product.image_url} alt={product.name} className="w-20 h-20 object-cover mb-2 rounded" />
                <h3 className="text-xl font-semibold text-blue-800">{product.name}</h3>
                <p className="text-lg text-gray-700">${typeof product.price === "number" ? product.price.toFixed(2) : product.price}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No products available.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Store;
