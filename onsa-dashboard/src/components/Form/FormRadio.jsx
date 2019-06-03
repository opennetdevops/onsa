import React from "react";
// import { Form } from ".";

const radio = props => {
  return (

    <div className="custom-control custom-radio custom-control-inline">
      <input
        id={props.id + "id"}
        name={props.groupName}
        type="radio"
        onChange={props.onChange}
        value={props.value}
        checked={props.selectedOption === props.value }
        className="custom-control-input"
        disabled={props.disabled || false}
      />
      <label className="custom-control-label" htmlFor={props.id + "id"}>
        {props.label}
      </label>
    </div>
  );
};

export default radio;
