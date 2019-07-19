import React from 'react';
import { Toast, ToastBody, ToastHeader } from 'reactstrap';
import PropTypes from 'prop-types';


const ResourcesCard = (props) => {
    // console.log("[Card - render]")
    return (
      <div className="p-2 rounded">
        <Toast>
          <ToastHeader className="text-muted h6 my-1" style={{letterSpacing: "0.1rem"}}>{props.title}</ToastHeader>
          <ToastBody className="text-left">
            {/* Customer Info, Access Node , Networking: */}
            <ul className="list-unstyled pl-2">
              {props.data.map(item => (
                <li key={item.field}>
                  <strong> {item.field}: </strong><label> {item.value}</label>
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