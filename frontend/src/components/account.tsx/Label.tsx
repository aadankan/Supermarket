const Label = (props: { children: any, center: boolean }) => {
  return (
    <div className={`w-full flex ${props.center ? "justify-center" : "justify-start"} text-white text-3xl [text-shadow:_0px_3px_3px_rgb(0,0,0,1)]`}>
      {props.children}
    </div>
  );
};

export default Label;
