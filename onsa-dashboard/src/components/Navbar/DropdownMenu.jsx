import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class DropdownMenu extends React.Component {

  static propTypes = {
  	className: PropTypes.string,
    bsClassName: PropTypes.string
  };
  
  static defaultProps = {
  	className: "dropdown-menu"
  };

  render() {

  	const { children, className, bsClassName, ...props} = this.props;
 
    return ( 	  
      <div className={classNames(className,bsClassName)} aria-labelledby="dropdown01" {...props}>
        {children}
      </div>
    );
  }
}

export default DropdownMenu;