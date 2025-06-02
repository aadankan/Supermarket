import Input from "./Input";
import Label from "./Label";

type LabelAndInput = {
  center?: boolean;
  inputType: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  labelText: string;
  placeholderText: string;
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
};

const LabelAndInput = ({center, inputType, value, onChange, labelText, placeholderText, onKeyDown}: LabelAndInput) => {
  return (
    <div className="w-full flex flex-col items-center gap-2">
      <Label center={center || false}>{labelText}</Label>
      <Input type={inputType} placeholder={placeholderText} value={value} onChange={onChange} onKeyDown={onKeyDown} />
    </div>
  );
};

export default LabelAndInput;
