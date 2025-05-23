const Email = () => {
  return (
    <div className="w-full flex flex-col justify-start items-start gap-3.5 overflow-hidden">
      <div className="w-full justify-start text-white text-3xl [text-shadow:_0px_3px_3px_rgb(0,0,0,1)]">
        Enter your email
      </div>
      <input className="w-[80%] p-4 h-14 relative bg-white/60 rounded-xl border-[1.50px] border-black" />
    </div>
  );
};
export default Email;
