import React from 'react';
import { Toast, ToastBody, ToastHeader } from 'reactstrap';
import PropTypes from 'prop-types';


const ResourcesCard = (props) => {
    
    return (
      <div className="p-2 my-2 ml-2 rounded">
        <Toast>
          <ToastHeader>{props.title}</ToastHeader>
          <ToastBody className="text-left">
            {/* Customer Info, Access Node , Networking: */}
            <ul>
              {props.data.map(item => (
                <li key={item.field}>
                  <strong> {item.field}:</strong> <span> {item.value} </span>
                </li>
              ))}
            </ul>
          </ToastBody>
        </Toast>
      </div>
    );
}
ResourcesCard.propTypes = {
    title: PropTypes.string.isRequired,
    data: PropTypes.arrayOf(PropTypes.shape({
        field: PropTypes.string.isRequired,
        value: PropTypes.string.isRequired
    })).isRequired
};


export default ResourcesCard;