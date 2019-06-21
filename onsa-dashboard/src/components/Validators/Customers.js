import * as yup from "yup";

export const validationSchema = () => {
    const clientMin = 3;
    const clientMax = 100;
    const clientErr =
      "Client Name must be between " +
      clientMin +
      " and " +
      clientMax +
      " characters long.";
    const cuicLength = 11;
    const cuicErr =
      "CUIC must be " +
      cuicLength +
      " numeric characters long, without spaces or any special characters.";

      yup.setLocale({string:{trim: "Check for leading and trailling spaces."}})

    let schema = yup.object({
      name: yup
        .string()
        .strict(true)
        .trim()
        .min(clientMin, clientErr)
        .max(clientMax, clientErr)
        .required(),
      cuic: yup
        .string()
        .length(cuicLength, cuicErr)
        .matches(/^[0-9]*$/, cuicErr)
        .required()
    });
    return schema;
  };

