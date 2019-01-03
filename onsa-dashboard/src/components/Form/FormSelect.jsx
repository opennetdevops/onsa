import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

class FormSelect extends React.Component {

  static propTypes = {

    className: PropTypes.string,
  };

  handleSelectChange = (event) => {

    this.props.onChange(event)

  }

  render() {
    const { children,
            className,
            ...props
      } = this.props

    return (
        <select className={classNames(className)} {...props}>             
          {children}
        </select>
    );
  }
};

export default FormSelect;




