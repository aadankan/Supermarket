import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import supermarketInside from "../assets/images/SupermarketInside.png";
import AdminPanel from "../components/account.tsx/AdminPanel";
import cart from "../assets/icons/cart.svg";
import cartBadged from "../assets/icons/cartBadged.svg";
import Product from "../components/store/Product";
import LogoutButton from "../components/account.tsx/LogoutButton";
import CartModal from "../components/Cart";
import OrdersModal from "../components/store/OrdersModal";

type ProductType = {
  id: number;
  name: string;
  price: number;
  image_url: string;
  category_id: number;
};

type CategoryType = {
  id: number;
  name: string;
};

type CartItemType = {
  product: ProductType;
  count: number;
};

type UserType = {
  id: number;
  email: string;
};

type OrderItemType = {
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

const Store = () => {
  const [cartActive, setCartActive] = useState(false);
  const [products, setProducts] = useState<ProductType[]>([]);
  const [categories, setCategories] = useState<CategoryType[]>([]);
  const [cartItems, setCartItems] = useState<CartItemType[]>([]);
  const [activeCategory, setActiveCategory] = useState<string>("");
  const [currentUser, setCurrentUser] = useState<UserType | null>(null);
  const [orders, setOrders] = useState<OrderItemType[]>([]);
  const [ordersModalActive, setOrdersModalActive] = useState(false);

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

  const getCategoryNameById = (id: number): string => {
    const found = categories.find((c) => c.id === id);
    return found ? found.name : "";
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
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching categories:", error);
      alert("Failed to fetch categories. Please try again later.");
    }
  };

  const fetchOrders = async (userId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/orders/user/${userId}`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (!response.ok) throw new Error("Błąd pobierania zamówień");
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching orders:", error);
      alert("Nie udało się pobrać zamówień.");
      return [];
    }
  };

  const fetchCurrentUser = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/users/me", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 401) {
        // token nieprawidłowy lub wygasł
        localStorage.removeItem("token");
        navigate("/login");
        return;
      }

      const data = await response.json();
      setCurrentUser(data);
    } catch (error) {
      console.error("Failed to fetch current user:", error);
      localStorage.removeItem("token");
      navigate("/login");
    }
  };

  useEffect(() => {
    fetchCurrentUser();

    const fetchData = async () => {
      const productsData = await getProducts();
      const categoriesData = await getCatergories();
      setProducts(productsData);
      setCategories(categoriesData);
    };

    fetchData();
  }, []);

  const addToCart = (product: ProductType, count: number) => {
    setCartItems((prevItems) => {
      const existingItem = prevItems.find((item) => item.product.id === product.id);
      if (existingItem) {
        return prevItems.map((item) =>
          item.product.id === product.id ? { ...item, count: item.count + count } : item
        );
      } else {
        return [...prevItems, { product, count }];
      }
    });
  };

  const removeFromCart = (productId: number) => {
    setCartItems((prev) => prev.filter((item) => item.product.id !== productId));
  };

  const updateItemCount = (productId: number, newCount: number) => {
    if (newCount <= 0) return removeFromCart(productId);
    setCartItems((prev) => prev.map((item) => (item.product.id === productId ? { ...item, count: newCount } : item)));
  };

  const placeOrder = async () => {
    if (cartItems.length === 0) return;

    if (!currentUser) {
      alert("Nie jesteś zalogowany. Zaloguj się, aby złożyć zamówienie.");
      return;
    }
    const userId = currentUser.id;
    const shippingAddressId = 1; // Replace with actual shipping address ID
    const billingAddressId = 1; // Replace with actual billing address ID

    try {
      const response = await fetch("http://localhost:8000/orders/with-items", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          user_id: userId,
          shipping_address_id: shippingAddressId,
          billing_address_id: billingAddressId,
          order_date: new Date().toISOString(),
          items: cartItems.map((item) => ({
            product_id: item.product.id,
            quantity: item.count,
            price: item.product.price,
          })),
        }),
      });

      if (!response.ok) throw new Error("Błąd składania zamówienia.");

      alert("Zamówienie zostało złożone!");
      setCartItems([]);
      setCartActive(false);
    } catch (err) {
      console.error(err);
      alert("Nie udało się złożyć zamówienia.");
    }
  };

  const showOrders = async () => {
    if (!currentUser) {
      alert("Nie jesteś zalogowany. Zaloguj się, aby zobaczyć swoje zamówienia.");
      return;
    }
    const userOrders = await fetchOrders(currentUser.id);
    setOrders(userOrders);
    setOrdersModalActive(true); // <-- poprawione, wcześniej było `false`
  };

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
          <LogoutButton logout={logout} />
        </div>
      </div>
      <div className="w-[80%] h-[80%] bg-white/80 p-8 rounded-xl shadow-lg flex flex-col items-center justify-start gap-4 overflow-hidden">
        <div className="w-full flex items-center justify-between px-4">
          <div>
            <h1 className="text-4xl font-bold text-blue-600 font-['Jacques_Francois_Shadow']">Welcome to the Store!</h1>
          </div>
          <div className="flex items-center justify-end gap-8">
            <button
              onClick={showOrders}
              className="p-3 rounded-full bg-white/50 text-blue-700 font-semibold hover:text-blue-900 hover:bg-gray-200 outline-2 cursor-pointer shadow-md transition-colors duration-300"
            >
              Moje zamówienia
            </button>

            <img
              src={cartItems.length > 0 ? cartBadged : cart}
              alt="Cart"
              className="w-12 h-12 cursor-pointer"
              onClick={() => setCartActive(!cartActive)}
            />
          </div>
        </div>
        <div className="w-full flex items-center justify-center bg-blue-200/50 outline-2 outline-blue-500 rounded-xl">
          {categories.length > 0 ? (
            <div className="flex justify-start items-center gap-4 overflow-x-auto px-2">
              <div
                className={`px-3 py-2 rounded-full cursor-pointer shadow-md ${
                  activeCategory === "" ? "bg-blue-900 text-white" : "bg-white text-blue-700"
                }`}
                onClick={() => setActiveCategory("")}
              >
                <h2 className="text-md font-semibold">Wszystkie</h2>
              </div>
              {categories.map((category) => (
                <div
                  key={category.id}
                  className={`px-3 py-2 rounded-full cursor-pointer shadow-md ${
                    activeCategory === category.name ? "bg-blue-900 text-white" : "bg-white text-blue-700"
                  }`}
                  onClick={() => setActiveCategory(category.name)}
                >
                  <h2 className="text-xl font-semibold">{category.name}</h2>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No categories available.</p>
          )}
        </div>
        <div className="w-full flex flex-wrap justify-center items-center gap-6 overflow-auto p-2">
          {products.length > 0 ? (
            products
              .filter((product) => activeCategory === "" || getCategoryNameById(product.category_id) === activeCategory)
              .map((product) => <Product key={product.id} product={product} addToCart={addToCart} />)
          ) : (
            <p className="text-gray-500">No products available.</p>
          )}
        </div>
      </div>
      {cartActive && (
        <CartModal
          cartItems={cartItems}
          onClose={() => setCartActive(false)}
          onRemove={removeFromCart}
          onUpdateCount={updateItemCount}
          onOrder={placeOrder}
        />
      )}
      {ordersModalActive && <OrdersModal orders={orders} onClose={() => setOrdersModalActive(false)} />}
    </div>
  );
};

export default Store;
