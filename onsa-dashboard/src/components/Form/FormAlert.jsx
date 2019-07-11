import React from "react";

//Stateless component to display messages within a <div>.

const customAlert = ({ dialogShow, dialogSuccess, dialogText, msgLabel }) => {
  //specify props: dialogSuccess:boolean and dialogText:string to display.
  //icnludeLabel prop: Overrides default label. dialogShow:boolean toogler

  let alertBox = null;

  if (dialogShow) {
    if (dialogSuccess === "info") {
      alertBox = (
        <div className="alert alert-info">
          <strong>{msgLabel ? msgLabel : "Attention: "}</strong>
          {dialogText}
        </div>
      );
    }
    else if (dialogSuccess) {
      alertBox = (
        <div className="alert alert-success">
          <strong>{msgLabel ? msgLabel : "Success! "}</strong>
          {dialogText}
        </div>
      );
    } else if (dialogSuccess === false) {
      alertBox = (
        <div className="alert alert-danger">
          <strong>{msgLabel ? msgLabel : "Something went wrong: "}</strong>
          {dialogText}
        </div>
      );
    } 
  }

  return alertBox;
};
export default customAlert;
