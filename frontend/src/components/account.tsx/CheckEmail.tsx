const CheckEmail = (props: {email: string}) => {
  return (
    <div className="inline-flex flex-col justify-start items-center gap-10">
      <div className="text-center justify-start text-white text-4xl font-normal font-['Inter'] drop-shadow-[0px_0px_4px_rgb(0,0,0,1)]">
        <p>Check your email to</p>
        <p>complete registration</p>
      </div>
      <div className="text-center justify-start text-white text-4xl font-normal font-['Inter'] drop-shadow-[0px_0px_4px_rgb(0,0,0,1)]">
        {props.email}
      </div>
    </div>
  );
};

export default CheckEmail;
