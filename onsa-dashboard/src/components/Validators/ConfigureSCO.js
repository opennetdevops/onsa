import * as yup from "yup";

export const validationSchema = () => {
    const min = 1;
    const max = 4094;
    const Err =
    "The Vlan Id must be an integer number between " +
    min +
    " and " +
    max +
    ".";
    yup.setLocale({string:{trim: "Check for leading and trailling spaces."}})

    let schema = yup.object({
      vlanId: yup
        .number()
        .nullable()
        .typeError(Err)
        .min(min, Err )
        .moreThan(min, Err)
        .max(max, Err )
        .integer(Err)
        .positive(Err)
    });
    return schema;
  };

