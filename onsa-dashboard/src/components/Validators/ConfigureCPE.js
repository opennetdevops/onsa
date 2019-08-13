import * as yup from "yup";

export const VALIDATAIONSCHEMA = () => {
    const min = 1;
		const max = 35;

		const ErrIp =
    "The IP address must be expressed in CIDR notation ";
    const Err =
    "The Serial number Id must be a string between " +
    min +
    " and " +
    max +
    "characters long.";

    yup.setLocale({string:{trim: "Check for leading and trailling spaces."}})

    let selectSchema = yup.string().required();

    let schema = yup.object({
        serialNumber: yup
        	.string()
          .required()
          .typeError(Err)
          .min(min, Err )
          .max(max, Err )
          .label("Serial Number"),	
				ipAddress: yup
        	.string()
          .required()
          .typeError(ErrIp)
          .matches(/^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$/i, ErrIp )
          .max(max, ErrIp )
          .label("IP Address"),	
				brand: selectSchema.label("Brand"),
				model: selectSchema.label("Device Model"),
    });
    return schema;
  };

