import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class NavDropdown extends React.Component {

  static propTypes = {
  	className: PropTypes.string,
    bsSuffix: PropTypes.string,
  	href: PropTypes.string,
  };
  
  static defaultProps = {
  	className: "nav-item dropdown"
  };

  render() {

  	const { children, className, bsSuffix, ...props} = this.props;
 
    return ( 	  
	    <li className={classNames(className,bsSuffix)} {...props}>
        {children}
      </li>
    );
  }
}

export default NavDropdown;