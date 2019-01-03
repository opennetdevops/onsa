import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class Collapse extends React.Component {

	static propTypes = {

		className: PropTypes.string,
		bsSuffix: PropTypes.string

	};

	static defaultProps = {

		className: "collapse"	
	};

	render() {

  	const { 
  					className,
  					bsSuffix,
  					children,
  					...props

  			 	} = this.props

    return ( 	  
	  <div className={classNames(className, bsSuffix)} {...props}>
	   	{children}
	  </div>
    );
  }
}

export default Collapse;