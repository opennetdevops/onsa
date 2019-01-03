import React from 'react';
import classNames from 'classnames';
import PropTypes from 'prop-types';


class Container extends React.Component {
  	
  static propTypes = {

  	className: PropTypes.string,
  	classSuffix: PropTypes.string,
  };

  static defaultProps = {
  	className: "container"
  };

  render() {

  	const { children,
  		    className,
  		    classSuffix,
  		    tag: Tag,
  		    ...props
  		  } = this.props;

    return ( 	  

			<Tag className={classNames(className, classSuffix)} {...props}>
        {children}              
      </Tag>
    );
  }
}

export default Container;









