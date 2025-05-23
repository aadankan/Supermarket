import React from "react";

const Input = (props: {type: string, value: string, placeholder: string, onChange: (e: React.ChangeEvent<HTMLInputElement>) => void}) => {
    return (
        <input
            type={props.type}
            className="w-full p-4 h-14 relative bg-white/60 rounded-xl border-2 border-black"
            value={props.value}
            placeholder={props.placeholder}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => props.onChange(e)}
        />
    )
}

export default Input;