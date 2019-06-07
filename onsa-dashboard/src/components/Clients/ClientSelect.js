import React, { Component } from 'react';

import AsyncSelect from 'react-select/lib/Async';


// const colourOptions = [
//     { value: 'chocolate', label: 'Chocolate' },
//     { value: 'strawberry', label: 'Strawberry' },
//     { value: 'vanilla', label: 'Vanilla' }
//   ]

// const filterColors = (inputValue ) => {
//     return colourOptions.filter(i =>
//       i.label.toLowerCase().includes(inputValue.toLowerCase())
//     );
//   };

//   const promiseOptions = inputValue =>
//   new Promise(resolve => {
//     setTimeout(() => {
//       resolve(filterColors(inputValue));
//     }, 1000);
//   }); 


 class ClientSelect extends Component {
    
    filterClients = (inputValue ) => {
        return this.props.clientOptions.filter(i =>
          i.label.toLowerCase().includes(inputValue.toLowerCase())
        );
      };

    clientList = inputValue =>  new Promise (resolve => {
        if (inputValue.length >= this.props.searchByMT) {resolve(this.filterClients(inputValue))}
    })

    render() {
      return (
        <AsyncSelect
         defaultOptions
         loadOptions={this.clientList}
         onChange={this.props.onChange}
         value= {this.props.value}
         placeholder= {"Search by " + this.props.searchByMT + " or more letters"}
         name={this.props.name}
         />
      );
    }
  };

  export default ClientSelect;