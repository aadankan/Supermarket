import Input from "./Input";
import Label from "./Label";

type PasswordProps = {
  center?: boolean;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
};

const Password = ({center, value, onChange}: PasswordProps) => {
  return (
    <div className="w-full">
      <Label center={center || false}>Enter your password</Label>
      <Input type="password" placeholder="Password" value={value} onChange={onChange} />
    </div>
  );
};

export default Password;
