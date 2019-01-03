import React from 'react';
import classNames from 'classnames';
import PropTypes from 'prop-types';

class NavItem extends React.Component {
  	
  static propTypes = {

  	className: PropTypes.string,
  	bsSuffix: PropTypes.string,
  };

  static defaultProps = {
  	className: "nav-item"
  };

  render() {

  	const { children,
  		    className,
  		    bsSuffix,
  		    ...props
  		  } = this.props;

    return ( 	  
	   <li className={classNames(className, bsSuffix)} {...props}>
	        {children}
	   </li>
    );
  }
}

export default NavItem;