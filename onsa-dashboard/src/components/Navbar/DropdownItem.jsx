import React from 'react';
import classNames from 'classnames';
import PropTypes from 'prop-types';

class DropdownItem extends React.Component {
  	
  static propTypes = {

  	className: PropTypes.string,
  	bsSuffix: PropTypes.string,
    href: PropTypes.string
  };

  static defaultProps = {
  	className: "dropdown-item"
  };

  render() {

  	const { children,
  		    className,
  		    bssClassName,
          href,
  		    ...props
  		  } = this.props;

    return ( 	  
	   <a className={classNames(className,bssClassName)} href={href} {...props}>{children}</a>
    );
  }
}

export default DropdownItem;