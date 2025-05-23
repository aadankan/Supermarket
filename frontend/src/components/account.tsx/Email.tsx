import React from "react";
import Input from "./Input";
import Label from "./Label";

type EmailProps = {
  center?: boolean;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
};

const Email = ({ center, value, onChange }: EmailProps) => {
  return (
    <div className={`w-[80%] flex flex-col items-start gap-3.5 overflow-hidden`}>
      <Label center={center || false}>
        Enter your email
      </Label>
      <Input
        type="email"
        placeholder="Email"
        value={value}
        onChange={onChange}
      />
    </div>
  );
};

export default Email;
