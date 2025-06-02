import exit from "../../assets/icons/exit.svg";

const LogoutButton = (props: { logout: () => void }) => {
  return (
    <div
      onClick={props.logout}
      className="w-[64px] h-16 relative bg-blue-600 rounded-2xl overflow-hidden hover:bg-blue-700 transition-colors cursor-pointer shadow-2xl"
    >
      <img src={exit} alt="Exit" className="p-2" />
    </div>
  );
};

export default LogoutButton;
