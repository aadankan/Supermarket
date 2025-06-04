import * as React from "react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import supermarketInside from "../assets/images/SupermarketInside.png";
import LogoutButton from "../components/account.tsx/LogoutButton";

import ProductsTable from "../components/adminPanel/ProductsTab";
import CategoriesTable from "../components/adminPanel/CategoriesTab";
import SuppliersTable from "../components/adminPanel/SuppliersTab";
import OrdersTable from "../components/adminPanel/OrdersTab";

const AdminPanelPage = () => {
  const [currentTab, setCurrentTab] = useState<string>("Orders");
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const goToStore = () => {
    navigate("/");
  };

  const tabs = ["Orders", "Products", "Categories", "Suppliers"];

  return (
    <div
      style={{ backgroundImage: `url(${supermarketInside})` }}
      className="w-screen h-screen flex flex-col bg-cover bg-bottom items-center justify-center gap-10"
    >
      {/* Top Bar */}
      <div className="w-[80%] flex justify-between items-center">
        <h1 className="text-amber-500 text-6xl font-['Jacques_Francois_Shadow'] [text-shadow:_0px_0px_5px_rgb(0_0_0_/_1.00)]">
          Supermarket
        </h1>
        <div className="flex gap-6">
          <button
            onClick={goToStore}
            className="px-5 h-16 bg-blue-600 text-white rounded-2xl text-3xl [text-shadow:_2px_2px_2px_rgb(0_0_0_/_1.00)] hover:bg-blue-700 transition-colors shadow-2xl outline-3 outline-blue-900 cursor-pointer"
          >
            Go to Store
          </button>
          <LogoutButton logout={logout} />
        </div>
      </div>

      {/* Main Panel */}
      <div className="w-[80%] h-[80%] bg-white/80 p-6 rounded-xl shadow-lg flex flex-col gap-4">
        <div className="w-full flex justify-between px-4">
          <h2 className="text-4xl font-semibold">Admin Panel</h2>
        </div>

        <div className="flex gap-[2%] h-[90%]">
          {/* Sidebar */}
          <div className="w-[20%] h-[98%] bg-amber-100/40 rounded-3xl p-4 flex flex-col gap-3 overflow-auto">
            {tabs.map((tab) => (
              <div
                key={tab}
                onClick={() => setCurrentTab(tab)}
                className={`w-full p-3 text-lg text-center rounded-2xl cursor-pointer transition-colors outline-2 shadow-md
                  ${
                    currentTab === tab ? "bg-amber-300/70 hover:bg-amber-300 font-bold" : "bg-white/70 hover:bg-white"
                  }`}
              >
                {tab}
              </div>
            ))}
          </div>

          {/* Content Area */}
          <div className="w-[76%] h-[98%] bg-amber-100/40 rounded-3xl p-4 overflow-auto">
            {currentTab === "Products" && <ProductsTable />}
            {currentTab === "Categories" && <CategoriesTable />}
            {currentTab === "Suppliers" && <SuppliersTable />}
            {currentTab === "Orders" && <OrdersTable />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPanelPage;
