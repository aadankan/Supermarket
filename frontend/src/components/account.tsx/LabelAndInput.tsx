import Input from "./Input";
import Label from "./Label";

type LabelAndInput = {
  center?: boolean;
  inputType: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  labelText: string;
  placeholderText: string;
};

const LabelAndInput = ({center, inputType, value, onChange, labelText, placeholderText}: LabelAndInput) => {
  return (
    <div className="w-full">
      <Label center={center || false}>{labelText}</Label>
      <Input type={inputType} placeholder={placeholderText} value={value} onChange={onChange} />
    </div>
  );
};

export default LabelAndInput;
