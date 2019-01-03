import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class FormInput extends React.Component {

  static propTypes = {

    className: PropTypes.string,
  };

  render() {
    const { children,
            className,
            bsSuffix,
            ...props
      } = this.props

    return (
        <input className={classNames(className)} {...props}/>
    );
  }
};

export default FormInput;




